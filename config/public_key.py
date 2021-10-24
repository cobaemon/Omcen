# -*- coding: utf-8 -*-
"""
Created on 2021/10/24 9:56:08

@author: cobalt
"""

import os

from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.PublicKey import RSA


class Rsa:
    # シークレットコードの読み込み
    # キーファイルの読み込み
    # シークレットコードを元にキーを復号
    def __init__(self, secret_code_path, rsa_key_path):
        with open(secret_code_path, mode='rb') as f:
            cipher_secret_code = f.read().split(b'\n')
        with open(rsa_key_path, mode='rb') as f:
            encoded_key = f.read()

        try:
            aes = AES.new(key=b'omcen service publickey password', mode=AES.MODE_EAX, nonce=cipher_secret_code[2])
            self.secret_code = aes.decrypt(cipher_secret_code[0])
            aes.verify(cipher_secret_code[1])
        except ValueError:
            return ValueError

        try:
            self.key = RSA.import_key(
                encoded_key, passphrase=self.secret_code
            )
        except (ValueError, IndexError, TypeError):
            return ValueError

    # RSAキーの生成
    # これを実行するとキーが再生成されるため以前に暗号化した暗号文は復号化できなくなるので注意
    # 特に本番環境での使用は秘密鍵の漏洩以外の状況では好ましくない
    def _generate(self):
        self.rsa_key = RSA.generate(3072)
        self.encrypted_key = self.rsa_key.export_key(
            passphrase=self.secret_code,
            pkcs=8,
            protection='PBKDF2WithHMAC-SHA1AndDES-EDE3-CBC'
        )

    # RSAキーの保存
    # RSAキーの再生成時の保存に利用すること
    def _save(self, save_path):
        if os.path.isfile(save_path):
            with open(save_path, mode='wb') as f:
                f.write(self.encrypted_key)
        else:
            return ValueError

    # 秘密鍵の生成
    # 秘密鍵の取得
    # 戻り値：bytes
    def _private_key(self):
        private_key = self.key.export_key()

        return private_key

    # 公開鍵の生成
    # 公開鍵の取得
    # 戻り値：bytes
    def public_key(self):
        public_key = self.key.publickey().export_key()

        return public_key

    # 暗号化
    # 引数：bytes, bytes
    # 戻り値：bytes
    def encryption(self, data, key):
        if type(data) != bytes or type(key) != bytes:
            return ValueError

        try:
            rsa = RSA.import_key(key)
            rsa_key = PKCS1_OAEP.new(rsa)
            cipher_data = rsa_key.encrypt(data)

            return cipher_data
        except ValueError:
            return ValueError

    # 復号化
    # 引数：bytes, bytes
    # 戻り値：bytes
    def decryption(self, cipher_data, key):
        if type(cipher_data) != bytes or type(key) != bytes:
            return ValueError

        try:
            rsa = RSA.import_key(key)
            rsa_key = PKCS1_OAEP.new(rsa)
            data = rsa_key.decrypt(cipher_data)

            return data
        except ValueError:
            return ValueError
