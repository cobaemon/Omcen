# -*- coding: utf-8 -*-
"""
Created on Wed Apr  7 23:03:06 2021

"""


class FilePathError(Exception):
    """指定した場所にファイルが存在しない場合のエラー"""
    message = '指定された場所にファイルが存在しません'


class RSAKeyImportError(Exception):
    """シークレットコードを元にRSAキーを生成できない場合のエラー"""
    message = '正常にRSAキーをインポートできません'


class ArgumentTypeError(Exception):
    """引数の型が正しくない場合のエラー"""
    message = '引数がbytes型ではありません'


class EncryptionError(Exception):
    """暗号化が失敗した場合のエラー"""
    message = '暗号化に失敗しました'


class DecryptionError(Exception):
    """復号化に失敗した場合のエラー"""
    message = '復号化に失敗しました'


class DataCorruptedError(Exception):
    """復号化したデータが改ざんされていた場合のエラー"""
    message = 'データが改ざんされている恐れがあります'
