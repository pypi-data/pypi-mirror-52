import argparse
import logging
import os
import requests
import yaml

from collections import namedtuple

from travail.utils import require

from toil.common import Toil
from toil.job import Job

Sample = namedtuple('Sample', ['id', 'phenotypes', 'sex', 'father', 'mother'])

logger = logging.getLogger(__name__)


def generate_manifest(url, samples, user, password, output):
    """

    :param url:
    :param samples:
    :param user:
    :param password:
    :param output:
    :return:
    """
    # TODO - complete
    pass


def parse_manifest(manifest_path):
    """

    :param manifest_path:
    :return:
    """
    pass


class ManifestGenerator:

    def __init__(self, url, user, password):
        self._url = url
        self._user = user
        self._password = password

    def generate(self, samples: list, output: str):
        """

        :param samples:
        :param output:
        :return:
        """
        with open(output, 'w') as fhandle:
            for sample in samples:
                # - create query URL using sample ID
                # - fetch response
                # - extract the required fields
                # - turn into line of the manifest
                response = self.query_for_rd3_subject(sample)
                records = self._parse_response(response)
                for record in records:
                    fhandle.write(record)
                    fhandle.write(os.linesep)

    def query_for_rd3_subject(self, subject_id):
        url = os.path.join(self._url, 'rd3_subject', subject_id)
        response = requests.get(url, auth=(self._user, self._password), verify=False)
        return response.json()

    @staticmethod
    def _parse_response(response: dict) -> list:
        # TODO - return list with PED-like lines
        print((response['phenotype'], response['disease'], response['identifier'], response['sex1']['identifier']))
        return list()


def generate_config():
    # TODO - complete
    pass


def run(args):
    """
    Entry point into this pipeline
    :param args: command line args
    :return:
    """
    require(os.path.exists(args.manifest),
            '{} not found. Please run "preprocess.py generate-manifest"'.format(args.manifest))
    require(os.path.exists(args.config),
            '{} not found. Please run "preprocess.py generate-config"'.format(args.config))
    # Parse families
    families = parse_manifest(args.manifest)

    # Parse config
    with open(args.config) as cfh:
        parsed_config = {x.replace('-', '_'): y for x, y in yaml.full_load(cfh.read()).items()}

    config = argparse.Namespace(**parsed_config)
    config.maxCores = int(args.maxCores) if args.maxCores else 8

    # Launch Pipeline
    with Toil(args) as toil:
        if not toil.options.restart:
            toil.start(Job.wrapJobFn(run_analyze, families, config))
        else:
            toil.restart()


def run_analyze(job, samples, config):
    """


    :param JobFunctionWrappingJob job: passed automatically by Toil
    :param dict[dict] samples: A nested dict of samples containing sample information
    :param Namespace config: Argparse Namespace object containing argument inputs
    """
    # job.addFollowOnJobFn(download_shared_files, samples, config)
    logger.info('Running analyze')
