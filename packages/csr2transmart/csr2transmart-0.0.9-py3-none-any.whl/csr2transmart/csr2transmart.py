import json
import logging
import sys
from os import path

import click
from transmart_loader.copy_writer import TransmartCopyWriter
from transmart_loader.transmart import DataCollection

from csr.csr import CentralSubjectRegistry, StudyRegistry
from csr.subject_registry_reader import SubjectRegistryReader
from csr.study_registry_reader import StudyRegistryReader
from csr2transmart.mappers.csr_mapper import CsrMapper
from csr2transmart.ontology_config import OntologyConfig

logger = logging.getLogger(__name__)


def read_configuration(config_dir) -> OntologyConfig:
    """ Parse configuration files and return set of dictionaries

    :param config_dir: Path to directory where the configs are stored
    """
    ontology_config_path = path.join(config_dir, 'ontology_config.json')
    if not path.exists(ontology_config_path) or not path.isfile(ontology_config_path):
        raise FileNotFoundError(f'Cannot find {ontology_config_path}')
    with open(ontology_config_path, 'r') as ontology_config_file:
        return OntologyConfig(**json.load(ontology_config_file))


def csr2transmart(input_dir: str,
                  output_dir: str,
                  config_dir: str,
                  study_id: str,
                  top_tree_node: str):

    try:
        logger.info('Reading configuration data...')
        ontology_config = read_configuration(config_dir)

        logger.info('Reading CSR data...')
        subject_registry_reader = SubjectRegistryReader(input_dir)
        subject_registry: CentralSubjectRegistry = subject_registry_reader.read_subject_registry()
        study_registry_reader = StudyRegistryReader(input_dir)
        study_registry: StudyRegistry = study_registry_reader.read_subject_registry()

        logger.info('Mapping CSR to Data Collection...')
        mapper = CsrMapper(study_id, top_tree_node)
        collection: DataCollection = mapper.map(subject_registry, study_registry, ontology_config.nodes)

        logger.info('Writing files to {}'.format(output_dir))
        copy_writer = TransmartCopyWriter(str(output_dir))
        copy_writer.write_collection(collection)

        logger.info('Done.')

    except Exception as e:
        print(e)
        sys.exit(1)


@click.command()
@click.argument('input_dir')
@click.argument('output_dir')
@click.argument('config_dir')
@click.version_option()
def run(input_dir, output_dir, config_dir):
    csr2transmart(
        input_dir,
        output_dir,
        config_dir,
        'CSR',
        '\\Central Subject Registry\\',
    )


def main():
    run()


if __name__ == '__main__':
    main()
