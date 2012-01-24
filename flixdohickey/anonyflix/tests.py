#!/usr/bin/env python
# encoding: utf-8
from django.test import TestCase
from django.utils import unittest

import time
import datetime

from flixdohickey.anonyflix.models import Movie 

class MovieObjTest(TestCase):
    def test_movie_synopsis(self):
        movie = Movie(movie_id=60020928)
        print movie.synopsis
        assert "Airheaded cheerleader Buffy" in movie.synopsis
    
    def test_series_seasons(self):
        movie = Movie(movie_id=70140365, series=True)
        print movie.seasons
        assert len(movie.seasons) == 7
    
    def test_movie_links(self):
        movie = Movie(movie_id=70140365, series=True)
        print movie.links
        assert 'seasons' in movie.links.keys()
    
    def test_season_links(self):
        movie = Movie(movie_id=70140365, series=True)
        for season in movie.seasons:
            print season
            print season.links
            assert 'discs' in season.links
        
    def test_season_discs(self):
        movie = Movie(movie_id=70140365, series=True)
        for season in movie.seasons:
            time.sleep(.5)
            print season.season_discs
        assert len(movie.seasons[0].season_discs) == 3
        assert len(movie.seasons[1].season_discs) == 6
    
    def test_season_episodes(self):
        movie = Movie(movie_id=70140365, series=True)
        season = movie.seasons[0]
        print season.episodes
        assert 'Prophecy Girl' in season.episodes[-1].title
    
    def test_series_episodes(self):
        show = Movie(movie_id=70140365, series=True)
        print show.episodes
        print "I can't believe we watched %s episodes of 'Buffy: The Vampire Slayer'" % len(show.episodes)
        assert 'Chosen' in show.episodes[-1].title
    
    def test_formats(self):
        movie = Movie(movie_id=60020928)
        print movie.formats
        assert 'DVD' in movie.formats
    
    def test_streaming(self):
        movie = Movie(movie_id=70034036)
        assert movie.streaming
        print movie.end_streaming
        assert movie.end_streaming == datetime.datetime(year=2012, month=2, day=12).date()
        