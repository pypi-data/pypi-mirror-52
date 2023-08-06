import logging
import os
import shutil
import yaml

from travail.utils import require, download_url_job
from travail.methods import create_fasta_dictionary, create_fasta_index

from toil.common import Toil
from toil.job import Job

logger = logging.getLogger(__name__)


def run(args):
    """
    This small pipeline takes a reference FASTA file and creates a sequence
    :param args: argparse.Namespace with parsed CLI args
    :return:
    """
    require(os.path.exists(args.config), '{} not found. Please run "preprocess.py generate-config"'.format(args.config))

    # Parse families
    # families = parse_manifest(args.manifest)
    families = dict()

    # Parse config
    with open(args.config) as cfh:
        config = {x.replace('-', '_'): y for x, y in yaml.full_load(cfh.read()).items()}

    config['maxCores'] = int(args.maxCores) if args.maxCores else 8

    # Pipeline sanity checks
    require(config['output_dir'], 'No output location specified: {}'.format(config['output_dir']))

    # Launch Pipeline
    with Toil(args) as toil:
        if not toil.options.restart:
            toil.start(Job.wrapJobFn(download_shared_files, families, config))
        else:
            toil.restart()


def download_shared_files(job, families, config, cores=1, memory='200M'):
    """Downloads files shared by all steps of the pipeline.

    """
    # fetch FASTA
    config['reference']['fa.gz'] = job.addChildJobFn(download_url_job, url=config['reference']['fa.gz'],
                                                     cores=cores, memory=memory).rv()
    job.addFollowOnJobFn(make_some_noise, families, config)


def make_some_noise(job, families, config):
    """

    :param job:
    :param families:
    :param config:
    :return:
    """
    # create sequence dictionary
    config['reference']['fa.gz.dict'] = job.addChildJobFn(create_fasta_dictionary, config['reference']['fa.gz']).rv()

    # create indices
    fasta_idx_job = job.addChildJobFn(create_fasta_index, config['reference']['fa.gz'])
    config['reference']['fa.gz.fai'] = fasta_idx_job.rv(0)
    config['reference']['fa.gz.gzi'] = fasta_idx_job.rv(1)
    job.addFollowOnJobFn(consolidate_output, families, config)


def consolidate_output(job, families, config):
    """
    Write the output (whatever it is) to the output directory.

    :param job:
    :param families:
    :param config:
    :return:
    """
    src = job.fileStore.readGlobalFile(config['reference']['fa.gz'])
    dest = os.path.join(config['output_dir'], 'reference.fa.gz')
    shutil.copy(src, dest)

    src = job.fileStore.readGlobalFile(config['reference']['fa.gz.dict'])
    dest = os.path.join(config['output_dir'], 'reference.dict')
    shutil.copy(src, dest)

    src = job.fileStore.readGlobalFile(config['reference']['fa.gz.fai'])
    dest = os.path.join(config['output_dir'], 'reference.fa.fai')
    shutil.copy(src, dest)

    src = job.fileStore.readGlobalFile(config['reference']['fa.gz.gzi'])
    dest = os.path.join(config['output_dir'], 'reference.fa.gzi')
    shutil.copy(src, dest)
