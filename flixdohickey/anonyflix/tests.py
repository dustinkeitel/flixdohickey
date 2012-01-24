#!/usr/bin/env python
# encoding: utf-8
from django.test import TestCase
from django.utils import unittest

from flixdohickey.anonyflix.models import Movie 

class MovieObjTest(TestCase):
    def test_movie_synopsis(self):
        movie = Movie(movie_id=60020928)
        print movie.synopsis
        
        raise NotImplementedError, "BUILD ME"