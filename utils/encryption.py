import os
import random
import struct
import hashlib
from Crypto.Cipher import AES

sixteen_mega_bytes = 16 * 1024 * 1024  # 16 MB


def encrypt(filename, file_size, key, to_file):
    """
    This function encrypt a given file.
    :param filename: the name of the file that will be encrypted.
    :param file_size: the size of the input file.
    :param key: the encryption key.
    :param to_file: the path of the file that the encryption will be saved in
    """
    # hash the key to produce equally long keys.
    key = hashlib.sha256(key.encode('utf-8')).digest()
    # generate random initial vector and convert it into bytes
    iv = ''.join([chr(random.randint(0, 0xFF)) for i in range(16)])
    iv = bytes(iv, encoding="raw_unicode_escape")
    # use AES algorithm to encrypt the file in block mode
    aes_encryptor = AES.new(key, AES.MODE_CBC, iv)
    with open(to_file, "wb") as encrypted_file:
        # write the iv and the file size at the beginning of the file
        encrypted_file.write(struct.pack('<Q', file_size))
        encrypted_file.write(iv)
        with open(filename, "rb") as file:
            # read file block by block and encrypt each block
            while True:
                data = file.read(sixteen_mega_bytes)
                n = len(data)
                if n == 0:
                    break
                elif n % 16 != 0:
                    # <- padded with spaces in the last block
                    data += b' ' * (16 - n % 16)
                encoded_data = aes_encryptor.encrypt(data)
                encrypted_file.write(encoded_data)


def decrypt(key, in_filename, out_filename=None):
    """
    This function decrypt a given file.
    :param key: decryption key.
    :param in_filename: the file the be decrypted.
    :param out_filename: the file that the decrypted data will be saved in.
    """
    if not out_filename:
        out_filename = os.path.splitext(in_filename)[0]
    key = hashlib.sha256(key.encode('utf-8')).digest()
    with open(in_filename, 'rb') as infile:
        # read the original file size and iv from the beginning of the file
        original_size = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, iv)
        # this variable is used to prevent errors.
        accumulating_size = 0
        with open(out_filename, 'wb') as outfile:
            while True:
                chunk = infile.read(sixteen_mega_bytes)
                accumulating_size += sixteen_mega_bytes
                if len(chunk) == 0:
                    break
                # temp fix
                elif len(chunk) % 16 != 0:
                    chunk += b' ' * (16 - len(chunk) % 16)
                outfile.write(decryptor.decrypt(chunk))
            if accumulating_size < original_size:
                print("failure in decryption")
                return
            outfile.truncate(original_size)
