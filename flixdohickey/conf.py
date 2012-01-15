#!/usr/bin/env python
# encoding: utf-8
"""
conf.py
"""
import sys
import os
sys.path.append(os.path.abspath(os.curdir))

from pyflix.Netflix import *
import flixdohickey.secretkey as secretkey


APP_NAME   = 'FlixDohickey'
API_KEY    = 'g2wcttragfgx37fv54qxpjqw'
API_SECRET = secretkey.get_api_secret()
CALLBACK   = ''

_client = None

def NFClient():
    return NetflixClient(APP_NAME, API_KEY, API_SECRET, CALLBACK)