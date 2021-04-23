from zfec import filefec
import os
import math


def get_erasure_coding_parameters(file_size):
    file_size = file_size / 1024.0  # KB
    shard_size = 8                  # KB
    while file_size/shard_size > 10:
        shard_size = shard_size * 2

    k = math.ceil(file_size/shard_size)                # number of data shards
    # print("file size:", file_size/1024, "MB")
    # print("shard size:", shard_size, "KB", shard_size/1024.0, "MB", shard_size/(1024.0*1024), "GB")
    # print("k: ", k)
    # print("Wasted", (shard_size*k - file_size)/1024, "MB")
    m = 3 + k
    return k, m


def encode(file, file_size, directory_to_write_shards, segment_number):
    if not os.path.exists(directory_to_write_shards):  # caller handles errors
        os.mkdir(directory_to_write_shards)            # make dir, read/write parts
    k, m = get_erasure_coding_parameters(file_size)
    print(k, m)
    shard_name = "shard_" + str(segment_number)
    filefec.encode_to_files(file, file_size, directory_to_write_shards, shard_name, k, m,
                            suffix=".fec", overwrite=False, verbose=False)


def decode(shards_directory, retrieved_segments_directory, segment_number, k):
    if not os.path.exists(retrieved_segments_directory):  # caller handles errors
        os.mkdir(retrieved_segments_directory)            # make dir, read/write parts
    i = 0
    shards = []
    shards_info = []
    shard_name = "shard_" + str(segment_number)
    k = k
    for filename in os.listdir(shards_directory):
        if filename.startswith(shard_name):
            shards.append(open(os.path.realpath(shards_directory+"/"+filename), 'rb'))
            shards_info.append(filename)
            if i >= k:
                break
            i += 1
    segment_name = "segment_" + str(segment_number)
    print(shards_info)
    segment_path = os.path.realpath(retrieved_segments_directory+"/"+segment_name)
    filefec.decode_from_files(open(segment_path, 'wb'), shards, verbose=False)
