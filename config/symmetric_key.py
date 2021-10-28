# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 10:12:06 2021

"""

from Crypto.Cipher import AES

from config.exception import DataCorruptedError


class Aes:
    def __init__(self, key):
        self.key = key

    # 暗号化
    # 引数：bytes
    # 戻り値：bytes, bytes, bytes
    def encryption(self, data):
        if type(data) != bytes:
            return ValueError
        elif data == b'':
            return b'', b'', b''

        try:
            aes = AES.new(self.key, AES.MODE_EAX)
        except ValueError:
            return ValueError

        cipherdata, tag = aes.encrypt_and_digest(data)

        return cipherdata, tag, aes.nonce

    # 復号化
    # 引数：bytes, bytes, bytes
    # 戻り値：
    def decryption(self, cipher_data, tag, nonce):
        if (type(cipher_data) != memoryview or
                type(tag) != memoryview or
                type(nonce) != memoryview):
            return None, ValueError
        elif cipher_data == b'':
            return b'', None

        try:
            aes = AES.new(self.key, AES.MODE_EAX, nonce)
        except ValueError:
            return None, ValueError

        try:
            data = aes.decrypt_and_verify(cipher_data, tag)
            return data, None
        except ValueError:
            return data, DataCorruptedError
