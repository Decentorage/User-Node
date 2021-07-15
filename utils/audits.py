import hashlib
import random
from .helper import Helper
helper = Helper()


def generate_hash(salt, filename):
    sha256_hash = hashlib.sha256()
    buffer_size = 65536  # read data in 64kb chunks
    with open(filename, "rb") as fn:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: fn.read(buffer_size), b""):
            sha256_hash.update(byte_block)
        sha256_hash.update(salt.encode())
    return sha256_hash.hexdigest()


def generate_audits(file, audits_count=helper.audits_default_count):
    for i in range(audits_count):
        salt = ''.join([chr(random.randint(0, 0xFF)) for i in range(16)])
        file_hash = generate_hash(salt, file)
