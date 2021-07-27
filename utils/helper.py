import os
import glob
import math
import json
from psutil import virtual_memory


class Helper:
    kilobyte = 1024
    megabyte = kilobyte * 1024
    gigabyte = megabyte * 1024

    def __init__(self):
        # define directories used in workspace.
        self.shards_directory_path = os.path.realpath("data/shards")
        self.segments_directory_path = os.path.realpath("data/segments")
        self.downloaded_output = os.path.realpath("data/downloaded data")
        self.encryption_directory = os.path.realpath("data/encrypted")
        self.cache_file = os.path.realpath("data/cache/decentorage_cache")
        self.transfer_file = os.path.realpath("data/cache/decentorage_transfer.json")
        self.download_transfer_file = os.path.realpath("data/cache/download_decentorage_transfer.json")
        self.upload_connection_file = os.path.realpath("data/cache/connections.txt")
        self.icon_path = os.path.realpath("gui/resources/decentorage_icon.png")
        self.shard_filename = "shard"
        self.segment_filename = "segment"
        self.send_chunk_size = int(0.5 * self.megabyte)
        self.receive_timeout = 8000
        self.disconnect_timeout = 1000*60*60

        # define some parameters used through the application
        self.host_url = "http://a9422c7200db042f59a56cdbf90ae1d2-2016308976.eu-central-1.elb.amazonaws.com:5000/"
        self.frontend_url = "http://decentorage.tech/user"
        self.client_url_prefix = 'user/'
        self.server_not_responding = "Check your internet connection"
        self.erasure_factor = 1
        self.minimum_data_shard = 2
        self.audits_default_count = 100
        self.upload_polling_time = 2
        self.min_price = 0.25
        self.state_upload_file = '1'
        self.state_upload_file_text = "Please enter your encryption key and start your upload"
        self.state_unpaid_pending_contract = '2'
        self.state_unpaid_pending_contract_text = 'Please add balance to the contract to start uploading'
        self.state_create_contract = '3'
        self.state_create_contract_text = "You have seeds, please select a file to upload"
        self.state_no_seeds = '4'
        self.state_no_seeds_text = "You have to request a seed before you can select a file to upload"
        self.token = None

        # mem = virtual_memory()
        # self.segment_size = math.floor(mem - int(2 * self.gigabyte))
        self.segment_size = int(500 * self.megabyte)                             # temporary value for test purposes

        # create directories if not exist.
        if not os.path.exists(self.shards_directory_path):
            os.makedirs(self.shards_directory_path)
        if not os.path.exists(self.encryption_directory):
            os.makedirs(self.encryption_directory)
        if not os.path.exists(self.segments_directory_path):
            os.makedirs(self.segments_directory_path)
        if not os.path.exists(self.downloaded_output):
            os.makedirs(self.downloaded_output)

    def get_encryption_file_path(self, filename):
        """
        This is a utility function to get the path of the encrypted file
        :param filename: the name of the encrypted file
        :return: encrypted file path
        """
        return os.path.realpath(self.encryption_directory + "/" + filename + ".enc")

    def reset_directories(self):
        """
        Delete content of temporary directories used in cleaning up the working space
        """
        files = glob.glob(self.segments_directory_path + '/*')
        for f in files:
            os.remove(f)
        files = glob.glob(os.path.realpath(self.encryption_directory) + '/*')
        for f in files:
            os.remove(f)

    def reset_shards(self):
        """
        Delete shards used in cleaning up the working space
        """
        files = glob.glob(self.shards_directory_path + '/*')
        for f in files:
            os.remove(f)

    def is_user_logged_in(self):
        """
        check if there is any cached tokens.
        :return: Boolean represents if the user is logged in or not.
        """
        try:
            cached_file = open(self.cache_file, 'r')
            self.token = cached_file.read()
            return True
        except:  # No cached token
            self.token = None
            return False

    def get_token(self):
        """
        Get cached token from file and save it to be used in the application requests.
        """
        try:
            cached_file = open(self.cache_file, 'r')
            self.token = cached_file.read()
        except:
            pass

    def get_erasure_coding_parameters(self, file_size):
        """
        Get k and m of the file that will be used in erasure coding
        :param file_size: the size of the input file
        :return: k and m
        """
        file_size = file_size / 1024.0  # KB
        shard_size = 8  # KB
        while file_size / shard_size > self.minimum_data_shard:
            shard_size = shard_size * 2

        # k: number of data shards
        k = self.minimum_data_shard  # math.ceil(file_size / shard_size)
        # m: total number of shards
        m = self.erasure_factor + k
        return k, m

    def get_file_metadata(self, file_size):
        """
        This function returns the file metadata needed by decentorage to save it
        :param file_size: size of the file
        :return: metadata of the file
        """
        # initialize the file metadata with empty segments array and their count
        file_metadata = {'segments': [], 'segments_count': math.ceil(int(file_size) / self.segment_size)}
        # append each segment parameters.
        for segment_index in range(file_metadata['segments_count'] - 1):
            k, m = self.get_erasure_coding_parameters(self.segment_size)
            segment = {'k': k, 'm': m, 'shard_size': math.ceil(self.segment_size/k)}
            file_metadata['segments'].append(segment)
        # append last segment details in the metadata
        k, m = self.get_erasure_coding_parameters(file_size -
                                                  self.segment_size*(file_metadata['segments_count'] - 1))
        segment = {'k': k, 'm': m, 'shard_size': math.ceil(
            math.ceil(file_size - self.segment_size*(file_metadata['segments_count'] - 1))/k)}
        file_metadata['segments'].append(segment)
        return file_metadata['segments'], file_metadata['segments_count']

    def read_transfer_file(self):
        """
        Read transfer file that is used to store information about the ongoing transfer
        :return: transfer dictionary
        """
        if not os.path.exists(self.transfer_file):
            return None
        else:
            outfile = open(self.transfer_file, 'r')
            transfer_obj = json.load(outfile)
            return transfer_obj

    def save_transfer_file(self, transfer_dict):
        """
        This function save the data in transfer file
        :param transfer_dict: transfer dictionary that will be saved
        """
        if not os.path.exists(self.transfer_file):
            raise Exception('Cache file deleted')
        else:
            outfile = open(self.transfer_file, 'w')
            json.dump(transfer_dict, outfile)

    def read_download_transfer_file(self):
        """
        Read download transfer file that is used to store information about the ongoing transfer
        :return: transfer dictionary
        """
        if not os.path.exists(self.download_transfer_file):
            return None
        else:
            outfile = open(self.download_transfer_file, 'r')
            transfer_obj = json.load(outfile)
            return transfer_obj

    def save_download_transfer_file(self, transfer_dict):
        """
        This function save the data in download transfer file
        :param transfer_dict: transfer dictionary that will be saved
        """
        if not os.path.exists(self.download_transfer_file):
            raise Exception('Cache file deleted')
        else:
            outfile = open(self.download_transfer_file, 'w')
            json.dump(transfer_dict, outfile)
