import os
import json
from .erasure_coding import encode, decode
from .encryption import encrypt, decrypt
from .helper import Helper
from .decentorage import get_pending_file_info
from .file_transfer_user import send_data, add_connection, check_old_connections
from time import sleep
helper = Helper()


def process_segment(from_file, key, segment_number, transfer_obj):
    if not transfer_obj['segments'][segment_number]['processed']:
        print("Segment#", segment_number, "--------Processing----------")
        # Encryption
        filename = os.path.basename(from_file)
        file_size = os.stat(from_file).st_size
        encrypted_file_path = helper.get_encryption_file_path(filename)
        encrypt(from_file, file_size, key, encrypted_file_path)

        # Erasure coding
        file_size = os.stat(encrypted_file_path).st_size
        input_file = open(from_file, 'rb')
        file_obj = input_file.read()
        encode(file_obj, file_size, helper.shards_directory_path, segment_number,
               transfer_obj['segments'][segment_number]['k'], transfer_obj['segments'][segment_number]['m'])
        input_file.close()

        # Rename Shards to their new ids
        shards = os.listdir(helper.shards_directory_path)
        shards_new = transfer_obj['segments'][segment_number]['shards']
        for shard_index, shard_name in enumerate(shards):
            os.rename(os.path.realpath(helper.shards_directory_path + '\\' + shard_name),
                      os.path.realpath(helper.shards_directory_path + '\\' + shards_new[shard_index]["shard_id"]))

        transfer_obj['segments'][segment_number]['processed'] = True
        save_transfer_file(transfer_obj)
    else:
        print("Segment#", segment_number, "--------Already Processed Resume uploading----------")
    # Upload Shards: Add connections and upload
    for shard_index, shard in enumerate(transfer_obj['segments'][segment_number]['shards']):
        if not shard['done_uploading']:
            print("Segment#", segment_number, "Shard#", shard_index, "--------Start Uploading.----------")
            req = {'type': 'upload',
                   'port': shard['port'],
                   'shard_id': os.path.realpath(helper.shards_directory_path + "\\" + shard['shard_id']),
                   'auth': shard['shared_authentication_key'],
                   'ip': shard['ip_address'],
                   "segment_number": segment_number,
                   "shard_index": shard_index
                   }
            # add_connection(req)
            sleep(3)
            # send_data(req, True)
            transfer_obj['segments'][segment_number]['shards'][shard_index]['done_uploading'] = True
            save_transfer_file(transfer_obj)
            print("Segment#", segment_number, "Shard#", shard_index, "--------Done Uploading.----------")
        else:
            print("Segment#", segment_number, "Shard#", shard_index, "--------Already Uploaded(Skipped)----------")

    # Reset
    helper.reset_shards()


def process_file(from_file, key, chunk_size=helper.segment_size):
    """
    This function divides the file into segments to process each segment separately
    :param from_file: input file that will be uploaded
    :param key: encryption key
    :param chunk_size: segment size
    """
    try:
        print("process file function")
        transfer_obj = read_transfer_file()
        response = get_pending_file_info()
        file_size = os.stat(from_file).st_size
        file_size_decentorage, segments_metadata = response['file_size'], response['segments']
        # First time to upload.
        if transfer_obj['start_flag']:
            print("First Upload")
            transfer_obj['segments'] = segments_metadata
            for segment_index, segment in enumerate(segments_metadata):
                transfer_obj['segments'][segment_index]['done_uploading'] = False
                transfer_obj['segments'][segment_index]['processed'] = False
            transfer_obj['key'] = key
            transfer_obj['start_flag'] = False
            save_transfer_file(transfer_obj)
        else:   # nothing to do just a debugging statement
            # check_old_connections()
            print("Resume Upload")
            key = transfer_obj['key']

        if file_size != file_size_decentorage:
            print("Invalid file")
            return
        if file_size < chunk_size:
            process_segment(from_file, key, 1, transfer_obj)
            return
        filename = os.path.basename(from_file)
        segment_num = 0
        input_file = open(from_file, 'rb')
        while 1:
            chunk = input_file.read(chunk_size)         # get next part <= chunk size
            if not chunk:                               # eof=empty string from read
                break
            print("Segment#", segment_num, "------START------")
            if not transfer_obj['segments'][segment_num]['done_uploading']:
                print("Segment#", segment_num, "Start Uploading.")
                file_segment_path = helper.segments_directory_path + '/' + str(segment_num) + '_' + filename
                file_segment = open(file_segment_path, 'wb')
                file_segment.write(chunk)
                process_segment(file_segment_path, key, segment_num, transfer_obj)
                file_segment.close()
                helper.reset_directories()
                transfer_obj['segments'][segment_num]['done_uploading'] = True
                save_transfer_file(transfer_obj)
                print("Segment#", segment_num, "Done Uploading. Cleaning up ....")
            else:
                print("Segment#", segment_num, "Already Uploaded(Skipped).")
            segment_num = segment_num + 1
        try:
            os.remove(helper.transfer_file)
        except:
            raise Exception("Error Occurred while deleting transfer file.")
        print("Done Processing and uploading file.")
        input_file.close()
    except:
        raise Exception("Error in process file")


def retrieve_original_file(key, file_metadata, read_size=helper.segment_size):
    """
    this function retrieve the file by decoding and decrypting different segments. Then combine segments into one file
    :param key: decryption key
    :param file_metadata: file metadata dictionary contain data needed to retrieve file
    :param read_size: segment size
    """
    if file_metadata['segments_count'] > 1:
        segment_num = 0
        while segment_num < file_metadata['segments_count']:
            segment_name = helper.segment_filename + '_' + str(segment_num)
            decode(helper.shards_directory_path, helper.segments_directory_path, segment_num, file_metadata['k'])
            decrypt(key, segment_name, segment_name + ".enc")
            segment_num += 1
    else:
        segment_name = helper.segment_filename + '_0'
        decode(helper.shards_directory_path, helper.segments_directory_path, 0, file_metadata['k'])
        decrypt(key, segment_name, segment_name + ".enc")

    output = open(file_metadata['filename'], 'wb')
    parts = os.listdir(helper.segments_directory_path)
    parts.sort()
    for filename in parts:
        file_path = os.path.join(helper.segments_directory_path, filename)
        file_obj = open(file_path, 'rb')
        while 1:
            file_bytes = file_obj.read(read_size)
            if not file_bytes:
                break
            output.write(file_bytes)
        file_obj.close()
    output.close()
    print("Done retrieving file")


def download_shards_and_retrieve(key, file_metadata, read_size=helper.segment_size):
    # TODO: shards to be downloaded

    retrieve_original_file(key, file_metadata, read_size=helper.segment_size)


def read_transfer_file():
    if not os.path.exists(helper.transfer_file):
        raise Exception('Cache file deleted')
    else:
        outfile = open(helper.transfer_file, 'r')
        transfer_obj = json.load(outfile)
        return transfer_obj


def save_transfer_file(transfer_obj):
    if not os.path.exists(helper.transfer_file):
        raise Exception('Cache file deleted')
    else:
        outfile = open(helper.transfer_file, 'w')
        json.dump(transfer_obj, outfile)
