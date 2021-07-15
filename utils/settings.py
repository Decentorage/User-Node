import os
import glob
import math


class Settings:
    kilobyte = 1024
    megabyte = kilobyte * 1024
    gigabyte = megabyte * 1024

    def __init__(self):
        # define directories used in workspace.
        self.shards_directory_path = os.path.realpath("shards")
        self.download_directory_path = os.path.realpath("download")
        self.segments_directory_path = os.path.realpath("segments")
        self.icon_path = os.path.realpath("gui/resources/decentorage_icon.png")
        self.encryption_directory = "encrypted"
        self.shard_filename = "shard"
        self.segment_filename = "segment"
        self.cache_file = os.path.realpath("data/decentorage_cache")
        self.upload_connection_file = os.path.realpath("data/connections.text")
        self.host_url = "http://192.168.1.3:5000/"
        self.client_url_prefix = 'user/'
        self.redirect_to_login = "Redirect to login"
        self.server_not_responding = "Check your internet connection"
        self.erasure_factor = 3
        self.minimum_data_shard = 4
        self.audits_default_count = 100
        self.upload_polling_time = 10
        self.state_upload_file = '1'
        self.state_upload_file_text = "Please start your upload"
        self.state_initiate_contract_instance = '2'
        self.state_initiate_contract_instance_text = "You have a pending contract, please select a file to upload"
        self.state_recharge = '3'
        self.state_recharge_text = "You have to request a contract before you can select a file to upload"
        self.token = None

        # self.segment_size = int(14 * self.gigabyte)                                   # 14 GBs max segment size
        self.segment_size = int(16 * self.megabyte)                                   # 5 MBs for test purposes

        # create directories if not exist.
        if not os.path.exists(self.shards_directory_path):
            os.makedirs(self.shards_directory_path)
        if not os.path.exists(self.download_directory_path):
            os.makedirs(self.download_directory_path)
        if not os.path.exists(self.encryption_directory):
            os.makedirs(self.encryption_directory)
        if not os.path.exists(self.segments_directory_path):
            os.makedirs(self.segments_directory_path)

    def get_encryption_file_path(self, filename):
        return os.path.realpath(self.encryption_directory + "/" + filename + ".enc")

    def reset_directories(self):
        """
        Delete content of temporary directories
        """
        files = glob.glob(self.shards_directory_path + '/*')
        for f in files:
            os.remove(f)
        files = glob.glob(self.segments_directory_path + '/*')
        for f in files:
            os.remove(f)
        files = glob.glob(os.path.realpath(self.encryption_directory) + '/*')
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
        return cached token.
        :return: token or none if no token exits.
        """
        try:
            cached_file = open(self.cache_file, 'r')
            self.token = cached_file.read()
        except:
            pass

    def get_erasure_coding_parameters(self, file_size):
        file_size = file_size / 1024.0  # KB
        shard_size = 8  # KB
        while file_size / shard_size > self.minimum_data_shard:
            shard_size = shard_size * 2

        k = math.ceil(file_size / shard_size)  # number of data shards
        m = self.erasure_factor + k
        return k, m

    def get_file_metadata(self, file_size):
        file_metadata = {'segments': [], 'segments_count': math.ceil(int(file_size) / self.segment_size)}
        for segment_index in range(file_metadata['segments_count'] - 1):
            k, m = self.get_erasure_coding_parameters(self.segment_size)
            segment = {'k': k, 'm': m, 'shard_size': math.ceil(self.segment_size/k)}
            file_metadata['segments'].append(segment)
        k, m = self.get_erasure_coding_parameters(file_size -
                                                  self.segment_size*(file_metadata['segments_count'] - 1))
        segment = {'k': k, 'm': m, 'shard_size': math.ceil(
            math.ceil(file_size - self.segment_size*(file_metadata['segments_count'] - 1))/k)}
        file_metadata['segments'].append(segment)
        return file_metadata['segments'], file_metadata['segments_count']
