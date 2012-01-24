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
            movie = Movie(json=info)
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
        if request.GET.get('series') == 'True':
            is_series = True
            
        movie = Movie(movie_id=request.GET['id'], series=is_series)
        
    return render_to_response('movie_detail.html', {'movie': movie})
    
def season_list(request):
    per_page = 10
    
    flix = []
    if 'id' in request.GET:
        series_id = request.GET['id']
        base_movie = Movie(movie_id=series_id, series=True)
        flix = base_movie.seasons
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
            
    return render_to_response('season_list.html', {'flix': movies})

def season_detail(request):
    """NOT DONE"""
    per_page = 10
    
    flix = []
    if 'series_id' in request.GET:
        series_id = request.GET['series_id']
        season_id = request.GET.get('season_id')
        link_base = '%sseries/%s/seasons/%s' % (ID_BASE, series_id, season_id)
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
            
    return render_to_response('season_detail.html', {'flix': movies})
        