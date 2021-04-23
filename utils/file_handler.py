import os
from .erasure_coding import encode
from .encryption import encrypt


def process_file(from_file, key):
    # Encryption
    filename = from_file.split("/")[-1]
    file_path = os.path.realpath(from_file)
    file_size = os.stat(file_path).st_size
    encrypt(file_path, file_size, key, os.path.realpath("temp/"+filename+".enc"))
    # Erasure coding
    file_path = os.path.realpath("temp/"+filename+".enc")
    file_size = os.stat(file_path).st_size
    input_file = open(from_file, 'rb')
    file_obj = input_file.read()
    encode(file_obj, file_size, os.path.realpath("shards"), 1)
    input_file.close()
