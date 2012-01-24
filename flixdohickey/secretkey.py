#!/usr/bin/env python
# encoding: utf-8
"""
secretkey.py

Solution taken from http://stackoverflow.com/a/4674143
"""
import os
import random

SETTINGS_ABSPATH = os.path.abspath(__file__)
PROJECT_BASE_DIR = os.path.dirname(SETTINGS_ABSPATH)

def get_api_secret():
    secret_key_file_path = os.path.join(PROJECT_BASE_DIR, 'netflix_secret_api.key')
    secret_key = open(secret_key_file_path, 'rb').read()
    return secret_key

def new_secret_key():
    character_pool = ''.join(
        [
            'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
            'abcdefghijklmnopqrstuvwxyz',
            '0123456789',
            '!@#$%^&*(-_=+)'
        ]
    )
    secret_key = ''.join(
        [random.choice(character_pool) for character in xrange(100)]
    )
    return secret_key


def get_secret_key(secret_key_file_path):
    if os.path.exists(secret_key_file_path) \
    and os.stat(secret_key_file_path).st_size:
        secret_key = open(secret_key_file_path, 'rb').read()
        return secret_key
    else:
        try:
            secret_key_file = open(secret_key_file_path, 'wb')
            secret_key_file.write(new_secret_key())
        finally:
            secret_key_file.close()
        get_secret_key(secret_key_file_path)