# -*- coding: utf-8 -*-

import logging
import os
import subprocess


def create_fasta_index(job, fasta_fid):
    """
    Run `samtools faidx reference.fa.gz` on provided gzipped FASTA file id.

    :param JobFunctionWrappingJob job: passed automatically by Toil
    :param fasta_fid: FileStoreId of gzipped FASTA file
    :return: tuple with FileStoreIds of FAI and GZI index files
    """
    work_dir = job.fileStore.getLocalTempDir()
    ref_fa = job.fileStore.readGlobalFile(fasta_fid, os.path.join(work_dir, 'reference.fa.gz'))

    command = ['samtools', 'faidx', ref_fa]

    cmd = ' '.join(command)
    job.log("Executing '{}'".format(cmd), logging.DEBUG)
    subprocess.check_call(cmd, shell=True)
    return (job.fileStore.writeGlobalFile(os.path.join(work_dir, 'reference.fa.gz.fai')),
            job.fileStore.writeGlobalFile(os.path.join(work_dir, 'reference.fa.gz.gzi')))


def create_fasta_dictionary(job, fasta_fid):
    """
    Run `samtools dict` on provided FASTA file and create FASTA sequence dictionary.

    :param JobFunctionWrappingJob job: passed automatically by Toil
    :param fasta_fid: FileStoreId of gzipped FASTA file
    :return: FileStoreId of the FASTA sequence dictionary
    """
    work_dir = job.fileStore.getLocalTempDir()
    ref_fa = job.fileStore.readGlobalFile(fasta_fid, os.path.join(work_dir, 'reference.fa.gz'))

    target_dict = os.path.join(work_dir, 'reference.dict')  # where to save the output

    command = ['samtools', 'dict', '-o', target_dict, ref_fa]
    cmd = ' '.join(command)
    job.log("Executing '{}'".format(cmd), logging.DEBUG)
    subprocess.check_call(cmd, shell=True)

    return job.fileStore.writeGlobalFile(os.path.join(target_dict))


def combine_gvcfs(job, config, sample_ids, gvcfs, gvcf_idxs):
    """

    :param JobFunctionWrappingJob job: passed automatically by Toil
    :param config:
    :param sample_ids: list of sample IDs
    :param gvcfs: list of file IDs pointing to gVCF files to merge
    :param gvcf_idxs: list of file IDs pointing to gVCF TBI files
    :return:
    """
    work_dir = job.fileStore.getLocalTempDir()

    # resources needed locally to perform gVCF merging
    ref_fa = os.path.join(work_dir, 'reference.fa.gz')
    job.fileStore.readGlobalFile(config['reference']['fa.gz'], ref_fa)
    ref_fai = os.path.join(work_dir, 'reference.fa.gz.fai')
    job.fileStore.readGlobalFile(config['reference']['fa.gz.fai'], ref_fai)
    ref_gzi = os.path.join(work_dir, 'reference.fa.gz.gzi')
    job.fileStore.readGlobalFile(config['reference']['fa.gz.gzi'], ref_gzi)

    vcf_files = []
    for sample_id, g_vcf_fid, g_vcf_tbi_fid in zip(sample_ids, gvcfs, gvcf_idxs):
        vcf_name = '{}.g.vcf.gz'.format(sample_id)
        vcf_path = os.path.join(work_dir, vcf_name)
        job.fileStore.readGlobalFile(g_vcf_fid, vcf_path)

        vcf_idx_name = '{}.g.vcf.gz.tbi'.format(sample_id)
        vcf_idx_path = os.path.join(work_dir, vcf_idx_name)
        job.fileStore.readGlobalFile(g_vcf_tbi_fid, vcf_idx_path)

        vcf_files.append("--variant {}".format(vcf_path))

    out_gvcf = os.path.join(work_dir, 'combined.g.vcf.gz')
    out_gvcf_tbi = os.path.join(work_dir, 'combined.g.vcf.gz.tbi')

    cmd = ['java', '-jar', '${EBROOTGATK}', '-T', 'CombineGVCFs',
           '--reference', ref_fa,
           '--out', out_gvcf,
           # '--create-output-variant-index', 'true',
           '--group', 'StandardAnnotation',
           '--tmp-dir', work_dir] + vcf_files
    r = ' '.join(cmd)
    subprocess.check_call(r, shell=True)

    return (job.fileStore.writeGlobalFile(out_gvcf),
            job.fileStore.writeGlobalFile(out_gvcf_tbi))


def perform_genotype_gvcf(job, config, gvcf, gvcf_idx):
    """

    :param JobFunctionWrappingJob job: passed automatically by Toil
    :return:
    """
    work_dir = job.fileStore.getLocalTempDir()

    # resources needed locally to perform variant calling
    ref_fa = os.path.join(work_dir, 'reference.fa.gz')
    job.fileStore.readGlobalFile(config['reference']['fa.gz'], ref_fa)
    ref_fai = os.path.join(work_dir, 'reference.fa.gz.fai')
    job.fileStore.readGlobalFile(config['reference']['fa.gz.fai'], ref_fai)
    ref_gzi = os.path.join(work_dir, 'reference.fa.gz.gzi')
    job.fileStore.readGlobalFile(config['reference']['fa.gz.gzi'], ref_gzi)

    in_gvcf = os.path.join(work_dir, 'samples.g.vcf.gz')
    job.fileStore.readGlobalFile(gvcf, in_gvcf)
    in_gvcf_tbi = os.path.join(work_dir, 'samples.g.vcf.gz.tbi')
    job.fileStore.readGlobalFile(gvcf_idx, in_gvcf_tbi)

    out_vcf = os.path.join(work_dir, 'genotyped.vcf.gz')
    out_vcf_tbi = os.path.join(work_dir, 'genotyped.vcf.gz.tbi')
    cmd = ['java', '-jar', '${EBROOTGATK}', '-T', 'GenotypeGVCFs',
           '-R', ref_fa,
           '--variant', in_gvcf,
           '--out', out_vcf,
           # '--create-output-variant-index', 'true',
           '--group', 'StandardAnnotation',
           '--tmp-dir', work_dir]

    r = ' '.join(cmd)
    subprocess.check_call(r, shell=True)

    return (job.fileStore.writeGlobalFile(out_vcf),
            job.fileStore.writeGlobalFile(out_vcf_tbi))


def perform_merge_vcfs_across_chromosomes(job, config, chromosomes, vcfs):
    """
    Use Picard MergeVcfs tool to merge VCFs in `vcfs` into a single VCF file.

    :param JobFunctionWrappingJob job: passed automatically by Toil
    :param config:
    :param chromosomes:
    :param vcfs:
    :return:
    """
    work_dir = job.fileStore.getLocalTempDir()

    # resources - we need sequence dictionary
    ref_dict = os.path.join(work_dir, 'reference.dict')
    job.fileStore.readGlobalFile(config['reference']['fa.gz.dict'], ref_dict)

    # inputs - VCFs to merge
    vcf_files = []
    for chromosome, vcf in zip(chromosomes, vcfs):
        vcf_name = "{}.vcf.gz".format(chromosome)
        vcf_path = os.path.join(work_dir, vcf_name)
        job.fileStore.readGlobalFile(vcf, vcf_path)
        vcf_files.append("INPUT={}".format(vcf_path))

    # output - single VCF file
    out_vcf = os.path.join(work_dir, 'combined.vcf.gz')
    out_vcf_tbi = os.path.join(work_dir, 'combined.vcf.gz.tbi')

    # prepare and run the command
    cmd = ['java', '-jar', '${EBROOTPICARD}/picard.jar', 'MergeVcfs',
           'SEQUENCE_DICTIONARY={}'.format(ref_dict), 'OUTPUT={}'.format(out_vcf)] + vcf_files
    r = ' '.join(cmd)
    subprocess.check_call(r, shell=True)

    return job.fileStore.writeGlobalFile(out_vcf), job.fileStore.writeGlobalFile(out_vcf_tbi)
