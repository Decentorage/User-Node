import os
from .erasure_coding import encode
from .encryption import encrypt
kilobytes = 1024
megabytes = kilobytes * 1024
size = int(100 * megabytes)  # 100 MBs


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


def divide_file_and_process(from_file, key, chunk_size=size):
    # Encryption
    filename = from_file.split("/")[-1]
    file_path = os.path.realpath(from_file)
    file_size = os.stat(file_path).st_size
    encrypt(file_path, file_size, key, os.path.realpath("temp/" + filename + ".enc"))

    segment_num = 0
    input_file = open(os.path.realpath("temp/" + filename + ".enc"), 'rb')
    while 1:
        chunk = input_file.read(chunk_size)  # get next part <= chunk size
        if not chunk:  # eof=empty string from read
            break
        segment_num = segment_num + 1
        encode(chunk, chunk_size, os.path.realpath("shards"), segment_num)
    input_file.close()
