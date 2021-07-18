import os
import random
import struct
import hashlib
from Crypto.Cipher import AES

sixteen_mega_bytes = 16 * 1024 * 1024  # 16 MB


def encrypt(filename, file_size, key, to_file):
    key = hashlib.sha256(key.encode('utf-8')).digest()
    iv = ''.join([chr(random.randint(0, 0xFF)) for i in range(16)])
    iv = bytes(iv, encoding="raw_unicode_escape")
    aes_key = AES.new(key, AES.MODE_CBC, iv)
    # print("ENCRYPTING:", file_size, iv, to_file)
    with open(to_file, "wb") as encrypted_file:
        encrypted_file.write(struct.pack('<Q', file_size))
        encrypted_file.write(iv)
        with open(filename, "rb") as file:
            while True:
                data = file.read(sixteen_mega_bytes)
                n = len(data)
                if n == 0:
                    break
                elif n % 16 != 0:
                    data += b' ' * (16 - n % 16)  # <- padded with spaces
                    # print("debugging chunk length:", n, len(data), len(data) % 16)
                encoded_data = aes_key.encrypt(data)
                encrypted_file.write(encoded_data)


def decrypt(key, in_filename, out_filename=None):
    if not out_filename:
        out_filename = os.path.splitext(in_filename)[0]
    # print("DECRYPTING: ", in_filename, out_filename, sixteen_mega_bytes)
    key = hashlib.sha256(key.encode('utf-8')).digest()
    with open(in_filename, 'rb') as infile:
        original_size = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        print("DECRYPTING: ", original_size, iv)
        decryptor = AES.new(key, AES.MODE_CBC, iv)

        with open(out_filename, 'wb') as outfile:
            while True:
                chunk = infile.read(sixteen_mega_bytes)
                if len(chunk) == 0:
                    break
                # temp fix
                elif len(chunk) % 16 != 0:
                    chunk += b' ' * (16 - len(chunk) % 16)
                outfile.write(decryptor.decrypt(chunk))
            # print("Done decoding, starts Truncating")
            outfile.truncate(original_size)
