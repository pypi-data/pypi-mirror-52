import argparse
import logging
import os
import shutil
import textwrap
import yaml

from collections import namedtuple, defaultdict

from travail.utils import require, download_url_job
from travail.methods import perform_genotype_gvcf, combine_gvcfs, perform_merge_vcfs_across_chromosomes, \
    create_fasta_index, create_fasta_dictionary

from toil.common import Toil
from toil.job import Job

Subject = namedtuple('Subject', ['family_id', 'subject_id', 'paternal_id', 'maternal_id', 'sex', 'affection',
                                 'experiment_id', 'base_dir'])
Family = namedtuple('Family', ['family_id', 'subjects'])

logger = logging.getLogger(__name__)

chromosomes = [str(chrom) for chrom in range(1, 23)] + ['X', 'Y', 'MT']


def generate_manifest():
    # TODO - figure out how the FAMILY_ID looks like
    return textwrap.dedent("""
            #   Edit this manifest to include information pertaining to each sample pair to be run.
            #   The first 6 fields of this manifest are the standard PED columns. The other columns denote experiment ID
            #   and path to base directory where the gVCF files can be found.
            #
            #   Family ID       Unique identifier of a family where subject belong to (e.g. `F1234567`)
            #   Subject ID      Unique identifier of the subject within SOLVE-RD (e.g. `P0000123`)
            #   Paternal ID     Subject ID of the paternal sample, 0 if not present
            #   Maternal ID     Subject ID of the maternal sample, 0 if not present
            #   Sex             1=male;2=female
            #   Affection       0=unknown;1=unaffected;2=affected
            #   Experiment ID   Unique identifier of the experiment within SOLVE-RD (e.g. `E0000456`)
            #   Base directory  Directory, where gVCF files corresponding to this Experiment ID are located
            #
            #
            #   Place your samples below, one per line.
            #
            #family_1	subject_1	paternal_id	maternal_id	sex	affection	experiment_id	path/to/base/dir
            """[1:])


def parse_manifest(manifest_path: str) -> dict:
    """
    Read manifest and decode lines into subjects. Then group the subjects into families and return in a dictionary
    stored by their `family_id`s.

    :param manifest_path: path to the manifest file
    :return: dict of gatk.Family objects to process
    """
    subjects = []
    with open(manifest_path) as fh:

        for line in fh:
            if line.startswith("#"):
                # skip comments
                continue

            tokens = line.strip().split('\t')
            if len(tokens) is not 8:
                logger.warning("Found {} columns instead of expected 8 in line '{}'".format(len(tokens), line))
                continue
            subjects.append(
                Subject(family_id=tokens[0], subject_id=tokens[1], paternal_id=tokens[2], maternal_id=tokens[3],
                        sex=tokens[4], affection=tokens[5], experiment_id=tokens[6], base_dir=tokens[7]))

    logger.info("Found {} entries in manifest".format(len(subjects)))

    families = defaultdict(dict)
    for subject in subjects:
        if subject.family_id not in families:
            families[subject.family_id]['family'] = Family(family_id=subject.family_id, subjects=[])
        families[subject.family_id]['family'].subjects.append(subject)

    return families


def generate_config():
    return textwrap.dedent("""
        # Example pipeline configuration
        #
        # Comments (beginning with #) do not need to be removed. Optional parameters left blank are treated as false.
        ####################################################################################################################
        # Required: URL to compressed reference genome
        reference:
            fa.gz: 

        system:
            # max number of cores used for selected jobs
            cores: 8

        # Where to write result files
        output-dir: /path/to/result/dir


        """[1:])


def run(args):
    """
    Entry point into the preprocess analysis.

    :param args: argparse.Namespace with parsed CLI args
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
        config = {x.replace('-', '_'): y for x, y in yaml.full_load(cfh.read()).items()}

    config['max_cores'] = int(args.maxCores) if args.maxCores else 8

    args.clean = 'always'  # TODO - remove when ready

    # Launch Pipeline
    with Toil(args) as toil:
        if not toil.options.restart:
            toil.start(Job.wrapJobFn(download_resources_and_samples, families, config))
        else:
            toil.restart()


def download_resources_and_samples(job, families, config, cores=1, memory='200M'):
    """Downloads files shared by all steps of the pipeline.

    """
    # fetch FASTA, index FASTA and create sequence dictionary
    fasta_job = job.addChildJobFn(download_url_job, url=config['reference']['fa.gz'])
    fasta_idx_job = fasta_job.addChildJobFn(create_fasta_index, fasta_job.rv())
    fasta_dict_job = fasta_job.addChildJobFn(create_fasta_dictionary, fasta_job.rv())

    config['reference']['fa.gz'] = fasta_job.rv()
    config['reference']['fa.gz.fai'] = fasta_idx_job.rv(0)
    config['reference']['fa.gz.gzi'] = fasta_idx_job.rv(1)
    config['reference']['fa.gz.dict'] = fasta_dict_job.rv()

    # download samples
    for family_id in families:
        # 1 - for each family
        family = families[family_id]['family']

        for subject in family.subjects:
            # 2 - for each subject of the family
            families[family_id][subject.experiment_id] = dict()
            families[family_id][subject.experiment_id]['gvcf'] = dict()
            families[family_id][subject.experiment_id]['gvcf_idx'] = dict()

            # 3 - for each chromosome
            for chrom in chromosomes:
                # create a file path to both gVCF and tabix index
                # e.g. `/path/to/E123456/E123456.X.g.vcf.gz`
                g_vcf_path = "{}.{}.g.vcf.gz".format(os.path.join(subject.base_dir, subject.experiment_id), chrom)
                g_vcf_url = "file:{}".format(g_vcf_path)
                families[family_id][subject.experiment_id]['gvcf'][chrom] = job.addChildJobFn(download_url_job,
                                                                                              url=g_vcf_url).rv()

                g_vcf_idx_path = "{}.{}.g.vcf.gz.tbi".format(os.path.join(subject.base_dir, subject.experiment_id),
                                                             chrom)
                g_vcf_idx_url = "file:{}".format(g_vcf_idx_path)
                families[family_id][subject.experiment_id]['gvcf_idx'][chrom] = job.addChildJobFn(download_url_job,
                                                                                                  url=g_vcf_idx_url).rv()

    job.addFollowOnJobFn(combine_gvcfs_within_family, families, config)


def combine_gvcfs_within_family(job, families, config):
    """
    Each subject/sample has variants in gVCF format in this step. There is a gVCF file for each chromosome.
    Here we combine gVCF files of family members into a single multisample gVCF file. The gVCF file and the TBI are then
    stored within `families[family_id]['all']['gvcf']` and `families[family_id]['all']['gvcf_idx']`, respectively.

    :param JobFunctionWrappingJob job: passed automatically by Toil
    :param families: A nested dict of families containing sample information
    :param config: Argparse Namespace object containing argument inputs
    :return:
    """
    for family_id in families:
        families[family_id]['all'] = dict()
        families[family_id]['all']['gvcf'] = dict()
        families[family_id]['all']['gvcf_idx'] = dict()

        for chromosome in chromosomes:
            exp_ids = [subject.experiment_id for subject in families[family_id]['family'].subjects]
            gvcfs = [families[family_id][exp_id]['gvcf'][chromosome] for exp_id in exp_ids]
            gvcf_idxs = [families[family_id][exp_id]['gvcf_idx'][chromosome] for exp_id in exp_ids]

            combine_job = job.addChildJobFn(combine_gvcfs, config, exp_ids, gvcfs, gvcf_idxs)
            families[family_id]['all']['gvcf'][chromosome] = combine_job.rv(0)
            families[family_id]['all']['gvcf_idx'][chromosome] = combine_job.rv(1)

    job.addFollowOnJobFn(genotype_gvcfs_within_chromosomes, families, config)


def genotype_gvcfs_within_chromosomes(job, families, config):
    """
    Now we have multisample gVCF file for each chromosome and family. Let's genotype the gVCF files in order to get the
    "regular" VCF files per chromosome.

    :param JobFunctionWrappingJob job: passed automatically by Toil
    :param families: A nested dict of families containing sample information
    :param config: Argparse Namespace object containing argument inputs
    :return:
    """
    for family_id in families:
        families[family_id]['all']['vcf'] = dict()
        families[family_id]['all']['vcf_idx'] = dict()

        for chromosome in chromosomes:
            gvcf = families[family_id]['all']['gvcf'][chromosome]
            gvcf_idx = families[family_id]['all']['gvcf_idx'][chromosome]

            genotype_job = job.addChildJobFn(perform_genotype_gvcf, config, gvcf, gvcf_idx)
            families[family_id]['all']['vcf'][chromosome] = genotype_job.rv(0)
            families[family_id]['all']['vcf_idx'][chromosome] = genotype_job.rv(1)

    job.addFollowOnJobFn(merge_vcfs_across_chromosomes, families, config)


def merge_vcfs_across_chromosomes(job, families, config):
    """
    Now we have multisample VCF file for each chromosome and family. Let's merge the VCF files into a single multisample
    VCF file containing variants on all chromosomes from all samples.

    :param JobFunctionWrappingJob job: passed automatically by Toil
    :param families: A nested dict of families containing sample information
    :param config: Argparse Namespace object containing argument inputs
    :return:
    """
    for family_id in families:
        families[family_id]['all']['merged'] = dict()

        # get VCF files of all chromosomes
        vcfs = [families[family_id]['all']['vcf'][chromosome] for chromosome in chromosomes]
        # TODO - remove if not required
        # vcf_idxs = [families[family_id]['all']['vcf_idx'][chromosome] for chromosome in chromosomes]

        merge_job = job.addChildJobFn(perform_merge_vcfs_across_chromosomes, config, chromosomes, vcfs)
        families[family_id]['all']['merged']['vcf'] = merge_job.rv(0)
        families[family_id]['all']['merged']['vcf_tbi'] = merge_job.rv(1)

    job.addFollowOnJobFn(consolidate_output, families, config)


def consolidate_output(job, families, config):
    """

    :param job:
    :param families:
    :param config:
    :return:
    """
    # copy result files into destination folders
    for family_id in families:
        # merged VCF file
        src = job.fileStore.readGlobalFile(families[family_id]['all']['merged']['vcf'])
        dest = os.path.join(config['output_dir'], '{}.vcf.gz'.format(family_id))
        shutil.copy(src, dest)

        # the index for the merged VCF file above
        src = job.fileStore.readGlobalFile(families[family_id]['all']['merged']['vcf_tbi'])
        dest = os.path.join(config['output_dir'], '{}.vcf.gz.tbi'.format(family_id))
        shutil.copy(src, dest)
