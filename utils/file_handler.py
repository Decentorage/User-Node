import os
from .erasure_coding import encode, decode
from .encryption import encrypt, decrypt
from .settings import Settings
from .file_transfer_user import send_data, add_connection
settings = Settings()


def process_file(from_file, key, segment_number):
    # Reset
    # settings.reset_directories()

    # Encryption
    filename = os.path.basename(from_file)
    file_size = os.stat(from_file).st_size
    encrypted_file_path = settings.get_encryption_file_path(filename)
    encrypt(from_file, file_size, key, encrypted_file_path)

    # Erasure coding
    file_size = os.stat(encrypted_file_path).st_size
    input_file = open(from_file, 'rb')
    file_obj = input_file.read()
    encode(file_obj, file_size, settings.shards_directory_path, segment_number)

    # Upload Shards
    shards = os.listdir(settings.shards_directory_path)
    for shard in shards:
        # TODO: Get parameters data
        ip = "192.168.1.7"
        req = {'type': 'upload',
               'port': int(5000),
               'shard_id': 'test1233',
               'auth': 'test1233'
               }
        # add_connection(req)
        # send_data(req, ip, True)
        # print(shard, " Sent !!")

    input_file.close()


def divide_file_and_process(from_file, key, chunk_size=settings.segment_size):
    """
    This function divides the file into segments to process each segment separately
    :param from_file: input file that will be uploaded
    :param key: encryption key
    :param chunk_size: segment size
    """
    filename = os.path.basename(from_file)
    segment_num = 0
    input_file = open(from_file, 'rb')
    while 1:
        chunk = input_file.read(chunk_size)         # get next part <= chunk size
        if not chunk:                               # eof=empty string from read
            break
        file_segment_path = settings.segments_directory_path + '/' + str(segment_num) + '_' + filename
        file_segment = open(file_segment_path, 'wb')
        file_segment.write(chunk)
        process_file(file_segment_path, key, segment_num)
        segment_num = segment_num + 1
        file_segment.close()
    input_file.close()


def retrieve_original_file(key, file_metadata, read_size=settings.segment_size):
    """
    this function retrieve the file by decoding and decrypting different segments. Then combine segments into one file
    :param key: decryption key
    :param file_metadata: file metadata dictionary contain data needed to retrieve file
    :param read_size: segment size
    """
    if file_metadata['segments_count'] > 1:
        segment_num = 0
        while segment_num < file_metadata['segments_count']:
            segment_name = settings.segment_filename + '_' + str(segment_num)
            decode(settings.shards_directory_path, settings.segments_directory_path, segment_num, file_metadata['k'])
            decrypt(key, segment_name, segment_name + ".enc")
            segment_num += 1
    else:
        segment_name = settings.segment_filename + '_0'
        decode(settings.shards_directory_path, settings.segments_directory_path, 0, file_metadata['k'])
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


def download_shards_and_retrieve(key, file_metadata, read_size=settings.segment_size):
    # TODO: shards to be downloaded

    retrieve_original_file(key, file_metadata, read_size=settings.segment_size)
