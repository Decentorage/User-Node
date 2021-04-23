import os
from .erasure_coding import encode, decode
from .encryption import encrypt, decrypt
kilobytes = 1024
megabytes = kilobytes * 1024
size = int(100 * megabytes)  # 100 MBs
shards_directory = os.path.realpath("shards")


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
        encode(chunk, chunk_size, shards_directory, segment_num)
    input_file.close()


def retrieve_original_file(from_dir, to_file, key, file_segmented, read_size=size):
    if file_segmented:
        segments_count = 1
        while segments_count < 5:  # 5 should be replaced with segments total count
            decode(shards_directory, from_dir, segments_count, 7)
            segments_count += 1
    else:
        decode(shards_directory, from_dir, 1, 7)

    output = open(to_file, 'wb')
    parts = os.listdir(from_dir)
    parts.sort()
    for filename in parts:
        file_path = os.path.join(from_dir, filename)
        file_obj = open(file_path, 'rb')
        while 1:
            file_bytes = file_obj.read(read_size)
            if not file_bytes:
                break
            output.write(file_bytes)
        file_obj.close()
    output.close()

    print("Erasure coding decode !!")
    decrypt(key, to_file, "out.mp4")
    print("Decrypting Done!")
