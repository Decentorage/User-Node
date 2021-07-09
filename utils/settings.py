import os
import glob
kilobyte = 1024
megabyte = kilobyte * 1024
gigabyte = megabyte * 1024


class Settings:
    def __init__(self):
        # define directories used in workspace.
        self.shards_directory_path = os.path.realpath("shards")
        self.download_directory_path = os.path.realpath("download")
        self.segments_directory_path = os.path.realpath("segments")
        self.encryption_directory = "encrypted"
        self.shard_filename = "shard"
        self.segment_filename = "segment"

        self.erasure_factor = 3

        self.segment_size = int(14 * gigabyte)                          # 14 GBs max segment size
        self.size = int(5 * megabyte)                                   # 5 MBs for test purposes

        # create directories of not exist.
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
