from zfec import filefec
import os
from .helper import Helper
helper = Helper()


def encode(file, file_size, directory_to_write_shards, segment_number, k_param, m_param):
    """
    This function encode a given file into 'm' shards.
    :param file: file object that will encoded.
    :param file_size: the file size.
    :param directory_to_write_shards: the path to the directory that the shards will be generated in.
    :param segment_number: the number of the segment being processed directly.
    :param k_param: data shards count.
    :param m_param: total shards count.
    """
    k, m = k_param, m_param
    shard_name = helper.shard_filename + '_' + str(segment_number)
    filefec.encode_to_files(file, file_size, directory_to_write_shards, shard_name, k, m,
                            suffix=".fec", overwrite=False, verbose=False)


def decode(shards_directory, retrieved_segments_directory, segment_number, k):
    """
    This function reads 'k' shards and decode them back to the segment.
    :param shards_directory: the path to the directory that the shards is saved at.
    :param retrieved_segments_directory: the path to the directory of that the retrieved segment will be saved in.
    :param segment_number: the number os the segment that will be retrieved
    :param k: data shards count
    """
    i = 0
    shards = []
    shard_name = helper.shard_filename + '_' + str(segment_number)
    for filename in os.listdir(shards_directory):
        if filename.startswith(shard_name):
            shards.append(open(os.path.realpath(shards_directory+"/"+filename), 'rb'))
            if i >= k:
                break
            i += 1
    segment_name = helper.segment_filename + '_' + str(segment_number)
    segment_path = os.path.join(retrieved_segments_directory, segment_name)
    filefec.decode_from_files(open(segment_path, 'wb'), shards, verbose=False)
