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
            req = NFClient().catalog.getTitle("%s%s" % (self.base_link(series), movie_id))
            try:
                self.json = req['catalog_title']
            except KeyError:
                print "Error! %s" % req
                raise
        else:
            self.json = json
        self.extended_info = {}
                                    
    def __str__(self):
        info = "<(%s (%s)\n" % (self.title, self.release_year)
        info += "%s\n" % self.box_art
        info += "Rated %s)>" % self.rating
        return info
    
    @lazyproperty
    def content(self):
        return pprint.pformat(json)
        
    @lazyproperty
    def title(self):
        return self.json['title']['regular']
        
    @lazyproperty
    def box_art(self):
        return self.json['box_art']['large']
        
    @lazyproperty
    def rating(self):
        return self.json['category'][0]['term']
        
    @lazyproperty
    def release_year(self):
        return self.json['release_year']
        
    @lazyproperty
    def id(self):
        return self.json['id'].split('/')[-1]
        
    @lazyproperty
    def disc(self):
        return NetflixDisc(self.json,NFClient())
        
    @lazyproperty
    def synopsis(self):
        return self.getInfo('synopsis')['synopsis']   
        
    @lazyproperty
    def web_link(self):
        return self.links['web page']     
        
    @property
    def is_series(self):
        if 'series' in self.json.get('id'):
            return True
        return False
    
    @property
    def is_season(self):
        if 'seasons' in self.json.get('id'):
            return True
        return False
    
    def getInfo(self, _type):
        if _type in self.extended_info:
            #print "%s cached!: %s" % (_type, str(self.extended_info[_type])[:100])
            return self.extended_info[_type]
        info = self.disc.getInfo(_type)
        self.extended_info[_type] = info
        #print "%s fresh!: %s" % (_type, str(self.extended_info[_type])[:100])
        return info
        
    @staticmethod
    def base_link(series):
        base = ID_BASE
        if series:
            base += 'series/'
        else:
            base += 'movies/'
        return base
    
    @lazyproperty
    def links(self):
        d = {}
        for link in self.json['link']:
            name = link['title']
            url = link['href']
            d[name] = url
        return d
    
    @lazyproperty
    def formats(self):
        these_formats = []
        if 'formats' not in self.links.keys():
            return these_formats
        format_data = self.getInfo('formats')
        if 'availability' in format_data.get('delivery_formats', {}):
            # If format_data['delivery_formats']['availability'] returns a dict, 
            # there's only one availability type.
            # If it's a list, if there are multiple availabilities
            if isinstance(format_data['delivery_formats']['availability'], list):
                for format in format_data['delivery_formats']['availability']:
                    this_format = format.get('category', {}).get('term', '')
                    these_formats.append(this_format)
            else:
                format = format_data['delivery_formats']['availability']
                this_format = format.get('category', {}).get('term', '')
                these_formats.append(this_format)
        return these_formats
    
    @lazyproperty
    def streaming(self):
        if 'instant' in self.formats:
            return True
        return False
    
    @lazyproperty
    def end_streaming(self):
        if not self.streaming:
            return None
        if not self.formats:
            return None
            
        format_data = self.getInfo('formats')
        if 'availability' not in format_data.get('delivery_formats', {}):
            return None
        # If it's a list, if there are multiple availabilities
        avail_data = format_data['delivery_formats']['availability']
        if isinstance(avail_data, list):
            for format in avail_data:
                this_format = format.get('category', {}).get('term', '')
                if this_format == 'instant':
                    if 'available_until' in format:
                        try:
                            return datetime.datetime.fromtimestamp(format['available_until']).date()
                        except TypeError:
                            return None
        else:
            # If format_data['delivery_formats']['availability'] returns a dict, 
            # there's only one availability type, and it must be streaming
            if 'available_until' in avail_data:
                try:
                    return datetime.datetime.fromtimestamp(format['available_until']).date()
                except TypeError:
                    return None
    
    @lazyproperty
    def printable_formats(self):
        return ', '.join(self.formats)
    
    @lazyproperty
    def seasons(self):
        seas = []
        if not self.is_series:
            return seas
        seasons = self.getInfo('seasons').get('catalog_titles', {}).get('catalog_title', [])
        for season in seasons:
            seas.append(Movie(json=season))
        return seas
    
    @lazyproperty
    def season_discs(self):
        if not self.is_season:
            return []
        season_discs = self.getInfo('discs').get('catalog_titles', {}).get('catalog_title', [])
        return [Movie(disc) for disc in season_discs]
    
    @lazyproperty
    def episodes(self):
        if not self.is_season and not self.is_series:
            return []
        return [Movie(ep) for ep in self.getInfo('episodes').get('catalog_titles', {}).get('catalog_title', [])]
        