#!/usr/bin/env python
# encoding: utf-8
"""
conf.py
"""
from pyflix.Netflix import *
import flixdohickey.secretkey as secretkey
import os

APP_NAME   = 'FlixDohickey'
API_KEY    = 'g2wcttragfgx37fv54qxpjqw'
API_SECRET = secretkey.get_api_secret()
CALLBACK   = ''

_client = None

def NFClient():
    return NetflixClient(APP_NAME, API_KEY, API_SECRET, CALLBACK)