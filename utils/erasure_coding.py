from zfec import filefec
import os
from .helper import Helper
helper = Helper()


def encode(file, file_size, directory_to_write_shards, segment_number):
    # TODO: get k, m from server.
    k, m = 4, 7
    shard_name = helper.shard_filename + '_' + str(segment_number)
    filefec.encode_to_files(file, file_size, directory_to_write_shards, shard_name, k, m,
                            suffix=".fec", overwrite=False, verbose=False)


def decode(shards_directory, retrieved_segments_directory, segment_number, k):
    i = 0
    shards = []
    shards_info = []
    shard_name = helper.shard_filename + '_' + str(segment_number)
    for filename in os.listdir(shards_directory):
        if filename.startswith(shard_name):
            shards.append(open(os.path.realpath(shards_directory+"/"+filename), 'rb'))
            shards_info.append(filename)
            if i >= k:
                break
            i += 1
    segment_name = helper.segment_filename + '_' + str(segment_number)
    print("Shards information: ", shards_info)
    segment_path = os.path.realpath(retrieved_segments_directory+"/"+segment_name)
    filefec.decode_from_files(open(segment_path, 'wb'), shards, verbose=False)
