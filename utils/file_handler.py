import os
from .erasure_coding import encode, decode
from .encryption import encrypt, decrypt
from .settings import Settings
settings = Settings()


def process_file(from_file, key, segment_number):
    # Reset
    settings.reset_directories()

    # Encryption
    filename = from_file.split("/")[-1]
    file_path = os.path.realpath(from_file)
    file_size = os.stat(file_path).st_size
    encrypted_file_path = settings.get_encryption_file_path(filename)
    encrypt(file_path, file_size, key, encrypted_file_path)

    # Erasure coding
    file_size = os.stat(encrypted_file_path).st_size
    input_file = open(from_file, 'rb')
    file_obj = input_file.read()
    encode(file_obj, file_size, settings.shards_directory_path, segment_number)
    input_file.close()


def divide_file_and_process(from_file, key, chunk_size=settings.size):
    """
    This function divides the file into segments to process each segment separately
    :param from_file: input file that will be uploaded
    :param key: encryption key
    :param chunk_size: segment size
    """
    file_path = os.path.realpath(from_file)
    filename = from_file.split('/')[-1]
    segment_num = 0
    input_file = open(file_path, 'rb')
    while 1:
        chunk = input_file.read(chunk_size)         # get next part <= chunk size
        if not chunk:                               # eof=empty string from read
            break
        segment_num = segment_num + 1
        file_segment_path = settings.segments_directory_path + '/' + str(segment_num) + '_' + filename
        file_segment = open(file_segment_path, 'wb')
        file_segment.write(chunk)
        process_file(file_segment_path, key, segment_num)
        file_segment.close()
    input_file.close()


def retrieve_original_file(key, file_metadata, read_size=settings.size):
    """
    this function retrieve the file by decoding and decrypting different segments. Then combine segments into one file
    :param key: decryption key
    :param file_metadata: file metadata dictionary contain data needed to retrieve file
    :param read_size: segment size
    """
    if file_metadata['segments_count'] > 1:
        segment_num = 1
        while segment_num <= file_metadata['segments_count']:
            segment_name = settings.segment_filename + '_' + str(segment_num)
            decode(settings.shards_directory_path, settings.segments_directory_path, segment_num, file_metadata['k'])
            decrypt(key, segment_name, segment_name + ".enc")
            segment_num += 1
    else:
        segment_name = settings.segment_filename + '_1'
        decode(settings.shards_directory_path, settings.segments_directory_path, 1, file_metadata['k'])
        decrypt(key, segment_name, segment_name + ".enc")

    output = open(file_metadata['filename'], 'wb')
    parts = os.listdir(settings.segments_directory_path)
    parts.sort()
    for filename in parts:
        file_path = os.path.join(settings.segments_directory_path, filename)
        file_obj = open(file_path, 'rb')
        while 1:
            file_bytes = file_obj.read(read_size)
            if not file_bytes:
                break
            output.write(file_bytes)
        file_obj.close()
    output.close()
    print("Done retrieving file")
