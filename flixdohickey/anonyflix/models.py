from django.db import models

import datetime
import pprint

from flixdohickey.conf import NFClient
from flixdohickey.utils import lazyproperty

from pyflix.Netflix import * 

ID_BASE = 'http://api.netflix.com/catalog/titles/'

class Movie(models.Model):
    def __init__(self, json=None, movie_id=None, series=False):
        assert json or movie_id, "Need either direct json object or a movie id to get"
        if not json and movie_id:
            self.json = NFClient().catalog.getTitle("%s%s" % (self.base_link(series), movie_id))['catalog_title']
        else:
            self.json = json
            
        self.content = pprint.pformat(json)
        self.title = self.json['title']['regular']
        self.box_art = self.json['box_art']['large']
        self.rating = self.json['category'][0]['term']
        self.release_year = self.json['release_year']
        self.id = self.json['id'].split('/')[-1]
        self.formats = []
        self.streaming = False
        self.end_streaming = None
        self.series = False
                
        self.web_link = None
        for link in self.json['link']:
            if link.get('title','') == 'web page':
                self.web_link = link['href']
                
        self.get_formats()
    
    def __str__(self):
        info = "<(%s (%s)\n" % (self.title, self.release_year)
        info += "%s\n" % self.box_art
        info += "Rated %s)>" % self.rating
        return info
        
    @property
    def is_series(self):
        if 'series' in self.json.get('id'):
            return True
        return False
    
    def getInfo(self, _type):
        return self.disc.getInfo(_type)
        
    @staticmethod
    def base_link(series):
        base = ID_BASE
        if series:
            base += 'series/'
        else:
            base += 'movies/'
        return base
    
    @lazyproperty
    def disc(self):
        return NetflixDisc(self.json,NFClient())
        
    @lazyproperty
    def synopsis(self):
        return self.getInfo('synopsis')['synopsis']
    
    def get_formats(self):
        has_avail_info = False
        for link in self.json['link']:
            if 'formats' in link.get('title', ''):
                has_avail_info = True
        if not has_avail_info:
            return
        format_data = self.getInfo('formats')
        if 'availability' in format_data.get('delivery_formats', {}):
            # If format_data['delivery_formats']['availability'] returns a dict, 
            # there's only one availability type.
            # If it's a list, if there are multiple availabilities
            if isinstance(format_data['delivery_formats']['availability'], list):
                for format in format_data['delivery_formats']['availability']:
                    self.process_one_format(format)
            else:
                format = format_data['delivery_formats']['availability']
                self.process_one_format(format)
    
    @lazyproperty
    def printable_formats(self):
        return ', '.join(self.formats)
    
    def process_one_format(self, format):
        this_format = format.get('category', {}).get('term', '')
        self.formats.append(this_format)
        if this_format == 'instant':
            self.streaming = True
            if 'available_until' in format:
                try:
                    self.end_streaming = datetime.datetime.fromtimestamp(format['available_until']).date()
                except TypeError:
                    pass
    
    @lazyproperty
    def seasons(self):
        seas = []
        if not self.is_series:
            return seas
        seasons = self.getInfo('seasons').get('catalog_titles', {}).get('catalog_title', [])
        for season in seasons:
            seas.append(Movie(json=season))
        return seas
            
        # disc_info = 
        #         return [Movie(disc) for disc in disc_info]    
            
            #seas = movie.getInfo('seasons')
            #         
            #         seasons = seas.get('catalog_titles', {}).get('catalog_title', [])
            #         for season in seasons:
            #             movie = Movie(season)
            #             season_disc = NetflixDisc(season,NFClient())
            #             #eps = season_disc.getInfo('episodes')
            #             season_discs = season_disc.getInfo('discs')['catalog_titles']['catalog_title']
            #             #movie.process_episodes(eps)
            #             movie.process_season_discs(season_discs)
            
        # disc_info = 
        #         return [Movie(disc) for disc in disc_info]
    
    def process_seasons(self, season_data):
        pass
    
    def process_episodes(self, ep_data):
        pass
    
    # def process_season_discs(self, disc_info):
    #         self.season_discs = 
            