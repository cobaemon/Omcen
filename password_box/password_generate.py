# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 03:37:39 2021

パスワード生成
"""

import secrets


def _generate(n=12, password_type=3):
    character = (
        '0123456789',
        'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
        '`˜!@#$%^&*()_+-={}[]\|:;"\'<>,.?/'
    )

    return ''.join([secrets.choice(''.join(character[:int(password_type)])) for _ in range(int(n))])
