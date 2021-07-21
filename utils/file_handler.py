import os
import sys
import time

from .erasure_coding import encode, decode
from .encryption import encrypt, decrypt
from .helper import Helper
from .decentorage import get_pending_file_info, start_download, file_done_uploading
from .file_transfer_user import send_data, add_connection, check_old_connections, receive_data
helper = Helper()


def process_segment(from_file, key, segment_number, transfer_obj, ui):
    """
    This function takes a segment then start to process it if it's not already processed, and start uploading shard
    by shard
    :param from_file: segment file that will be processed
    :param key: encryption key used to encrypt segment
    :param segment_number: segment number in a file
    :param transfer_obj: transfer object that holds information about transaction.
    """
    # If the segment is not processed, process it
    if not transfer_obj['segments'][segment_number]['processed']:
        print("Segment#", segment_number, "--------Processing----------")
        # Process#1:    Encryption
        try:
            filename = os.path.basename(from_file)
            file_size = os.stat(from_file).st_size
            encrypted_file_path = helper.get_encryption_file_path(filename)
            encrypt(from_file, file_size, key, encrypted_file_path)
            print("Segment Encrypted")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            function_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Error in Encryption", exc_type, function_name, exc_tb.tb_lineno)
            return
        # Process#2:    Erasure coding
        try:
            file_size = os.stat(encrypted_file_path).st_size
            input_file = open(encrypted_file_path, 'rb')
            file_obj = input_file.read()
            encode(file_obj, file_size, helper.shards_directory_path, segment_number,
                   transfer_obj['segments'][segment_number]['k'], transfer_obj['segments'][segment_number]['m'])
            input_file.close()
            print("Segment Erasure coded")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            function_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Error in Erasure coding", exc_type, function_name, exc_tb.tb_lineno)
            return
        # Process#2:    Rename Shards to their new ids
        try:
            shards = os.listdir(helper.shards_directory_path)
            shards_new = transfer_obj['segments'][segment_number]['shards']
            for shard_index, shard_name in enumerate(shards):
                os.rename(os.path.realpath(helper.shards_directory_path + '\\' + shard_name),
                          os.path.realpath(helper.shards_directory_path + '\\' + shards_new[shard_index]["shard_id"]))
            print("Shards Renamed")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            function_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Error in renaming shards", exc_type, function_name, exc_tb.tb_lineno)
            return

        # Segment is processed save it's new state
        transfer_obj['segments'][segment_number]['processed'] = True
        helper.save_transfer_file(transfer_obj)
    # If the segment is already processed, Nothing to do just a debugging statement
    else:
        print("Segment#", segment_number, "--------Already Processed Resume uploading----------")

    # Upload Shards: Add connections and upload
    for shard_index, shard in enumerate(transfer_obj['segments'][segment_number]['shards']):
        # If shard is not uploaded
        if not shard['done_uploading']:
            print("Segment#", segment_number, "Shard#", shard_index, "--------Start Uploading.----------")
            # Prepare upload information dictionary
            req = {'type': 'upload',
                   'port': shard['port'],
                   'shard_id': os.path.realpath(helper.shards_directory_path + "\\" + shard['shard_id']),
                   'auth': shard['shared_authentication_key'],
                   'ip': shard['ip_address'],
                   "segment_number": segment_number,
                   "shard_index": shard_index
                   }
            # Add connection
            add_connection(req)

            # Send data to storage node
            send_data(req, True, ui)

            # Save new state of the shard
            # transfer_obj['segments'][segment_number]['shards'][shard_index]['done_uploading'] = True
            # save_transfer_file(transfer_obj)
            print("Segment#", segment_number, "Shard#", shard_index, "--------Done Uploading.----------")

        else:
           print("Segment#", segment_number, "Shard#", shard_index, "--------Already Uploaded(Skipped)----------")

    # Reset
    # helper.reset_shards()


def process_file(from_file, key, ui, chunk_size=helper.segment_size):
    """
    This function divides the file into segments to process each segment separately
    :param from_file: input file that will be uploaded
    :param key: encryption key
    :param chunk_size: segment size
    :param ui: ui object
    """
    # try:
    print("process file function")
    # Get needed data to start processing and uploading.
    transfer_obj = helper.read_transfer_file()
    response = get_pending_file_info(ui)
    file_size = os.stat(from_file).st_size
    file_size_decentorage, segments_metadata = response['file_size'], response['segments']

    # First time to upload.
    if transfer_obj['start_flag']:
        print("First Upload")
        helper.reset_shards()
        helper.reset_directories()
        transfer_obj['segments'] = segments_metadata
        # Add segment state
        for segment_index, segment in enumerate(segments_metadata):
            transfer_obj['segments'][segment_index]['done_uploading'] = False
            transfer_obj['segments'][segment_index]['processed'] = False
        transfer_obj['key'] = key
        transfer_obj['start_flag'] = False
        helper.save_transfer_file(transfer_obj)
    else:   # Retry uploading on pending connections
        print("Resume Upload")
        if transfer_obj['key']:
            key = transfer_obj['key']
        else:
            return
        check_old_connections(ui)

    # File path has been changed
    if file_size != file_size_decentorage:
        print("Invalid file")
        return

    # File size is smaller than chunk size, 1 segment is needed
    if file_size < chunk_size:
        print("Segment", "Start Uploading.")
        process_segment(from_file, key, 0, transfer_obj, ui)
        helper.reset_directories()
        transfer_obj['segments'][0]['done_uploading'] = True
        helper.save_transfer_file(transfer_obj)
        print("Segment", "Done Uploading. Cleaning up ....")
        try:
            os.remove(helper.transfer_file)
        except:
            raise Exception("Error Occurred while deleting transfer file.")
        print("Done Processing and uploading file.")
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
            process_segment(file_segment_path, key, segment_num, transfer_obj, ui)
            file_segment.close()
            helper.reset_directories()
            transfer_obj['segments'][segment_num]['done_uploading'] = True
            helper.save_transfer_file(transfer_obj)
            print("Segment#", segment_num, "Done Uploading. Cleaning up ....")
        else:
            print("Segment#", segment_num, "Already Uploaded(Skipped).")
        segment_num = segment_num + 1
    try:
        os.remove(helper.transfer_file)
    except:
        raise Exception("Error Occurred while deleting transfer file.")
    print("Done Processing and uploading file.")
    file_done_uploading(ui)
    input_file.close()
    #except Exception as e:
    #    exc_type, exc_obj, exc_tb = sys.exc_info()
    #    filename = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    #    print(exc_type, filename, exc_tb.tb_lineno)


def retrieve_original_file(key, info, read_size=helper.segment_size):
    """
    this function retrieve the file by decoding and decrypting different segments. Then combine segments into one file
    :param info: file metadata dictionary contain data needed to retrieve file
    :param key: decryption key
    :param read_size: segment size
    """
    segments_count = len(info["segments"])
    if segments_count > 1:
        for segment_num, segment in enumerate(info["segments"]):
            segment_name = helper.segment_filename + '_' + str(segment_num)
            print("-----------------Decoding Segment#" + str(segment_num) + "-----------------")
            decode(helper.shards_directory_path, helper.encryption_directory, segment_num, segment['k'])
            print("-----------------Decrypting Segment#" + str(segment_num) + "-----------------")
            decrypt(key, os.path.join(helper.encryption_directory, segment_name),
                    os.path.join(helper.segments_directory_path, segment_name))
    else:
        segment_name = helper.segment_filename + '_0'
        print("-----------------Decoding Segment#0-----------------")
        decode(helper.shards_directory_path, helper.encryption_directory, 0, info["segments"][0]['k'])
        print("-----------------Decrypting Segment#0-----------------")
        decrypt(key, os.path.join(helper.encryption_directory, segment_name),
                os.path.join(helper.segments_directory_path, segment_name))

    print("-----------------Retrieve file-----------------")
    output = open(os.path.join(helper.downloaded_output, info['filename']), 'wb')
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
    print("-----------------Done Retrieving File-----------------")


def download_shards_and_retrieve(filename, key, ui, progress_bar, read_size=helper.segment_size):
    """
    This function download shards needed to retrieve the file and then call retrieve original file function
    :param progress_bar: progress bar to show the percentage of download
    :param filename: the name of the file to be downloaded.
    :param key: the decryption key that will be used to decrypt the files.
    :param ui: ui object.
    :param read_size: segment size
    """
    print("-----------------Request Download from Decentorage ----------------")
    # get information of the shards to download them
    segments = start_download(filename, ui)
    if segments:
        for segment in segments:
            for shard in segment['shards']:
                req = {'type': 'download',
                       'port': int(shard['port']),
                       'shard_id': shard['shard_id'],
                       'auth': shard['auth'],
                       'ip': shard['ip_address']
                        }
                print("-----------------Downloading Shard#"+str(shard['shard_no'])+" in Segment#" +
                      str(shard['segment_no'])+"----------------")
                progress_bar(segment['shard_size'])
                # Add connection
                add_connection(req)
                # Receive data to storage node
                receive_data(req)
                print("-----------------Download Done ----------------")
    else:
        return
    try:
        # rename the shards to their original names.
        print("-----------------Shards Renaming----------------")
        for segment in segments:
            for shard in segment['shards']:
                os.rename(os.path.join(helper.shards_directory_path, shard['shard_id']),
                          os.path.join(helper.shards_directory_path,
                                       helper.shard_filename + "_" + str(shard['segment_no']) + "." +
                                       str(shard['shard_no']) + "_" + str(segment["m"])))
        print("-----------------Shards Renamed-----------------")
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        function_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print("Error in renaming shards", exc_type, function_name, exc_tb.tb_lineno)
        return
    # prepare file metadata dictionary needed by retrieve original file function.
    file_metadata = {
        "filename": filename,
        "segments": segments
    }
    print("-----------------Start retrieving-----------------")
    retrieve_original_file(key, file_metadata, read_size)
    print("-----------------Done retrieving-----------------")
    print("-----------------Cleaning up-----------------")
    helper.reset_directories()
    helper.reset_shards()
    ui.stackedWidget.setCurrentWidget(ui.main_page)
