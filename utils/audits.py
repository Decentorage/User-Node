import hashlib
import random
from .helper import Helper
helper = Helper()


def generate_hash(salt, filename):
    """
    Utility function for generate audits function that generate hash for a specific file
    :param salt: salt to be combined with the file
    :param filename: the name of the file that will be hashed
    :return: the hash of the file combined with the salt
    """
    sha256_hash = hashlib.sha256()
    # read data in 64kb chunks
    buffer_size = 65536
    # open file
    with open(filename, "rb") as fn:
        # read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: fn.read(buffer_size), b""):
            sha256_hash.update(byte_block)
        sha256_hash.update(salt.encode())
    return sha256_hash.hexdigest()


def generate_audits(file, audits_count=helper.audits_default_count):
    """
    This function generate audits to a given file
    :param file: input file that will need audits
    :param audits_count: number of audits to be generated
    :return: list of audits
    """
    audits = []
    for i in range(audits_count):
        # generate random salt of length 16 bytes
        salt = ''.join([chr(random.randint(0, 0xFF)) for i in range(16)])
        # get hash
        file_hash = generate_hash(salt, file)
        # append to audits list
        audits.append({"salt": salt, "hash": file_hash})
    return audits
