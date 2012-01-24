from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('flixdohickey.anonyflix.views',
    url(r'^$', 'home', name='home'),
    url(r'^basic_search', 'search_by_string', name='search_by_string'),
    #url(r'^basic_search(?P<search_term>\.+$)', 'search_by_string', name='search_by_string'),
    url(r'^movie_detail/', 'movie_detail', name='movie_detail'),
    url(r'^season_list/', 'season_list', name='season_list'),
     url(r'^season_detail/', 'season_detail', name='season_detail'), 
)

urlpatterns += patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
