import json
import logging
from datetime import datetime
from math import isnan
from os import path
from typing import Any, Tuple, Dict, Union, Sequence
from csr.csr import CentralSubjectRegistry, StudyRegistry, SubjectEntity, StudyEntity
from csr.tsv_reader import TsvReader
from sources2csr.codebook_mapper import CodeBookMapper
from sources2csr.data_exception import DataException
from sources2csr.sources_config import SourcesConfig


logger = logging.getLogger(__name__)


def format_column(column: Union[str, Tuple[str, str]]):
    if isinstance(column, str):
        return column.lower()
    return column[0].lower() if column[1] == '' else column[1].lower()


def format_value(schema: Dict, column: str, value: Any):
    if column not in schema['properties']:
        return None
    if isinstance(value, float) and isnan(value):
        return None
    return value


def transform_entity(values: Dict[Any, Any], schema: Dict) -> Dict:
    return {format_column(k): format_value(schema, format_column(k), v)
            for k, v in values.items()}


def transform_entities(entities: Any, schema: Dict, constructor: Any):
    entities = [transform_entity(entity, schema) for entity in entities]
    return [constructor(entity) for entity in entities]


def read_configuration(config_dir) -> SourcesConfig:
    """ Parse configuration files and return set of dictionaries

    :param config_dir: Path to directory where the configs are stored
    """
    sources_config_path = path.join(config_dir, 'sources_config.json')
    if not path.exists(sources_config_path) or not path.isfile(sources_config_path):
        raise DataException(f'Cannot find {sources_config_path}')
    with open(sources_config_path, 'r') as sources_config_file:
        return SourcesConfig(**json.load(sources_config_file))


class SourcesReader:

    def __init__(self, input_dir, output_dir, config_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.sources_config = read_configuration(config_dir)

    def read_source_file_data(self, source_file) -> Sequence[Dict[str, Any]]:
        source_file_data = TsvReader(path.join(self.input_dir, source_file)).read_data()
        if self.sources_config.codebooks is not None:
            codebook_filename = self.sources_config.codebooks.get(source_file, None)
            if codebook_filename is not None:
                codebook_mapper = CodeBookMapper(path.join(self.input_dir, codebook_filename))
                source_file_data = codebook_mapper.apply(source_file_data)
        return source_file_data

    def read_entity_data(self, entity_type) -> Sequence:
        """
        Reads data for an entity type from the source files that are specified
        in the sources config file.

        :param entity_type: the entity type, e.g., Individual.
        :return: A sequence of entities.
        """
        logger.info(f'* Reading {entity_type.__name__} data ...')
        if entity_type.__name__ not in self.sources_config.entities:
            raise DataException(f'No source configuration found for the {entity_type.__name__} entity')
        entity_sources_config = self.sources_config.entities[entity_type.__name__]
        source_columns = list([attribute.name for attribute in entity_sources_config.attributes])
        logger.debug(f'Source columns: {source_columns}')
        schema = entity_type.schema()
        schema_columns = list(schema['properties'].keys())
        logger.debug(f'Schema columns: {schema_columns}')
        invalid_columns = set(source_columns) - set(schema_columns)
        if invalid_columns:
            raise DataException(f'Unknown columns in source configuration: {invalid_columns}')
        id_column = list([name for (name, prop) in schema['properties'].items()
                          if 'identity' in prop and prop['identity'] is True])[0]
        logger.debug(f'Id column: {id_column}')

        source_files = set([source.file
                            for attribute in entity_sources_config.attributes
                            for source in attribute.sources])
        source_file_id_mapping = dict([(source.file, source.column if source.column is not None else attribute.name)
                                       for attribute in entity_sources_config.attributes
                                       for source in attribute.sources
                                       if attribute.name == id_column])
        logger.debug(f'Source files: {source_files}')
        logger.debug(f'Source file id mapping: {source_file_id_mapping}')

        source_files_without_id_column = source_files - set(source_file_id_mapping.keys())
        if source_files_without_id_column:
            raise DataException(f'Id column missing in source files: {source_files_without_id_column}')

        source_data = {}
        entity_data = {}
        for source_file in source_files:
            source_file_data = self.read_source_file_data(source_file)
            source_id_column = source_file_id_mapping[source_file]
            for item in source_file_data:
                item_id = item[source_id_column]
                if item_id not in entity_data:
                    entity_data[item_id] = {id_column: item_id}
            source_data[source_file] = source_file_data

        logger.debug(f'{entity_type.__name__} entity data: {entity_data}')

        for attribute in entity_sources_config.attributes:
            if not attribute.name == id_column:
                # add data to entities for attribute
                logger.debug(f'Adding data for attribute {attribute.name}')
                for source in attribute.sources:
                    # default column name is the attribute name
                    source_column = source.column if source.column is not None else attribute.name
                    # add data from source to attribute
                    logger.debug(
                        f'Adding data for attribute {attribute.name} from source {source.file}:{source_column}')
                    source_id_column = source_file_id_mapping[source.file]
                    for entity_id, entity in entity_data.items():
                        if attribute.name not in entity or entity[attribute.name] is None:
                            source_records = list([record for record in source_data[source.file]
                                                   if record[source_id_column] == entity_id])
                            if len(source_records) > 1:
                                raise DataException(f'Multiple records for {entity_type.__name__}'
                                                    f' with id {entity_id} in file {source.file}')
                            if len(source_records) == 1:
                                value = source_records[0][source_column]
                                if value == '':
                                    value = None
                                if value is not None and source.date_format is not None:
                                    value = datetime.strptime(value, source.date_format)
                                entity[attribute.name] = value

        logger.debug(f'{entity_type.__name__} entity data: {entity_data}')

        return transform_entities(
            entity_data.values(),
            entity_type.schema(),
            lambda e: entity_type(**e)
        )

    def read_subject_data(self) -> CentralSubjectRegistry:
        logger.info('Reading subject registry data ...')

        subject_registry_data: Dict[str, Sequence[SubjectEntity]] = {}

        for entity_type in list(SubjectEntity.__args__):
            subject_registry_data[entity_type.__name__] = self.read_entity_data(entity_type)

        return CentralSubjectRegistry.create(subject_registry_data)

    def read_study_data(self) -> StudyRegistry:
        logger.info('Reading study registry data ...')

        study_registry_data = {}

        for entity_type in list(StudyEntity.__args__):
            study_registry_data[entity_type.__name__] = self.read_entity_data(entity_type)

        return StudyRegistry.create(study_registry_data)
