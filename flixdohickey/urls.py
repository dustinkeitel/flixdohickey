from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'flixdohickey.anonyflix.views.home', name='home'),
    url(r'^basic_search/', 'flixdohickey.anonyflix.views.search_by_string', name='search_by_string'),
    url(r'^movie_detail/', 'flixdohickey.anonyflix.views.movie_detail', name='movie_detail'),
    url(r'^season_detail/', 'flixdohickey.anonyflix.views.season_detail', name='season_detail'),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
