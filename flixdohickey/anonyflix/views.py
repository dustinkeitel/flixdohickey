import simplejson as json

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.contrib import messages
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from flixdohickey.conf import NFClient
from flixdohickey.anonyflix.models import Movie

import sys, os
sys.path.append(os.path.abspath(os.curdir))
from pyflix.Netflix import *

ID_BASE = 'http://api.netflix.com/catalog/titles/'

def home(request):
    return render_to_response('home.html')

def search_by_string(request):
    per_page = 10
    start = 0
    end = 50
    
    flix = []
    term = ''
    if 'search_term' in request.GET:
        term = request.GET['search_term']
        data = NFClient().catalog.searchTitles(term,start,end)
        for info in data:
            #deep_data = NFClient().catalog.getTitle(info['id'])
            movie = Movie(info)
            flix.append(movie)
    paginator = Paginator(flix, per_page)
    try:
        page = int(request.GET.get('page',1))
    except ValueError:
        page = 1
    
    try:
        movies = paginator.page(page)
    except (EmptyPage, InvalidPage):
        movies = paginator.page(paginator.num_pages)
            
    return render_to_response('basic_search.html', {'flix': movies, 'search_term' : term})

def movie_detail(request):
    if 'id' in request.GET:
        is_series = False
        link_base = ID_BASE + 'movies/'
        if request.GET['series'] == 'True':
            is_series = True
            link_base = ID_BASE + 'series/'
            
        base_data = NFClient().catalog.getTitle("%s%s" % (link_base, request.GET['id']))
        movie = Movie(base_data['catalog_title'])
        
        disc = NetflixDisc(base_data['catalog_title'],NFClient())
        if is_series:
            seas = disc.getInfo('seasons')
            print seas
            movie.process_seasons(seas)
        else:
            formats = disc.getInfo('formats')
            movie.process_formats(formats)
        
    return render_to_response('movie_detail.html', {'movie': movie})
    
def season_detail(request):
    per_page = 10
    
    flix = []
    if 'id' in request.GET:
        series_id = request.GET['id']
        link_base = ID_BASE + 'series/'
        data = NFClient().catalog.getTitle("%s%s" % (link_base, series_id))
        disc = NetflixDisc(data['catalog_title'],NFClient())
        seas = disc.getInfo('seasons')
        seasons = seas.get('catalog_titles', {}).get('catalog_title', [])
        for season in seasons:
            movie = Movie(season)
            season_disc = NetflixDisc(season,NFClient())
            #eps = season_disc.getInfo('episodes')
            season_discs = season_disc.getInfo('discs')['catalog_titles']['catalog_title']
            #movie.process_episodes(eps)
            movie.process_season_discs(season_discs)
            flix.append(movie)
    for flik in flix:
        print flik
            
    paginator = Paginator(flix, per_page)
    try:
        page = int(request.GET.get('page',1))
    except ValueError:
        page = 1
    
    try:
        movies = paginator.page(page)
    except (EmptyPage, InvalidPage):
        movies = paginator.page(paginator.num_pages)
            
    return render_to_response('season_detail.html', {'flix': flix})
        