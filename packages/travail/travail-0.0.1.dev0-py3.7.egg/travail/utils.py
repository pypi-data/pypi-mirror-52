import os
import shutil
import subprocess

import travail.pp.phenopackets_pb2 as pp
import google.protobuf.json_format as jf

from six.moves.urllib import parse


class UserError(Exception):
    pass


def require(expression, message):
    if not expression:
        raise UserError('\n\n' + message + '\n\n')


def generate_file(content_provider, file_path: str) -> None:
    """
    Generate file with content provided by `content_provider`.
    :param content_provider: function that returns content that is supposed to be written into the file
    :param file_path: where the output should be written. ValueError is risen if the path points to an existing destination
        that is not a file
    :return: None
    """
    if os.path.exists(file_path) and not os.path.isfile(file_path):
        msg = "Refusing to write output to path '{}' which already exists and is not a file".format(file_path)
        raise ValueError(msg)

    with open(file_path, 'w') as fh:
        fh.write(content_provider())


def download_url_job(job, url, name=None):
    """Job version of `download_url`"""
    work_dir = job.fileStore.getLocalTempDir()
    fpath = download_url(url, work_dir=work_dir, name=name)
    return job.fileStore.writeGlobalFile(fpath)


def download_url(url, work_dir='.', name=None):
    """
    Downloads URL, can pass in file://, http://, s3://, or ftp://, gnos://cghub/analysisID, or gnos:///analysisID
    If downloading S3 URLs, the S3AM binary must be on the PATH

    :param str url: URL to download from
    :param str work_dir: Directory to download file to
    :param str name: Name of output file, if None, basename of URL is used
    :return: Path to the downloaded file
    :rtype: str
    """
    file_path = os.path.join(work_dir, name) if name else os.path.join(work_dir, os.path.basename(url))

    pr = parse.urlparse(url)
    if pr.scheme == 'file':
        shutil.copy(pr.path, file_path)
    else:
        subprocess.run(['curl', '-fs', '--retry', '5', '--create-dir', url, '-o', file_path])
    assert os.path.exists(file_path)
    return file_path


def parse_phenopacket_json(json_payload: str) -> pp.Phenopacket:
    """
    Parse JSON string containing Phenopacket data.

    :param json_payload: string with JSON content to be decoded
    :return: Phenopacket with data decoded from `json_payload`
    """
    return jf.Parse(json_payload, pp.Phenopacket())


def parse_family_json(json_payload: str) -> pp.Family:
    """
    Parse JSON string containing Family data.

    :param json_payload: string with JSON content to be decoded
    :return: Family with data decoded from `json_payload`
    """
    return jf.Parse(json_payload, pp.Family())


def check_command_is_available(cmd):
    pass