from django.db import models

import datetime
import pprint

ID_BASE = 'http://api.netflix.com/catalog/titles/'

class Movie(models.Model):
    def __init__(self, json):
        
        
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
    
    def process_formats(self, format_data):
        if 'availability' in format_data.get('delivery_formats', {}):
            # If format_data['delivery_formats']['availability'] can return a dict, if there's only one availability
            # type, or a list, if there are multiple availabilities
            if isinstance(format_data['delivery_formats']['availability'], list):
                for format in format_data['delivery_formats']['availability']:
                    self.process_one_format(format)
            else:
                format = format_data['delivery_formats']['availability']
                self.process_one_format(format)
                
        self.formats = sorted(self.formats)
        self.printable_formats = ', '.join(self.formats)
    
    def process_seasons(self, season_data):
        pass
    
    def process_episodes(self, ep_data):
        pass
    
    def process_season_discs(self, disc_info):
        self.season_discs = [Movie(disc) for disc in disc_info]
            