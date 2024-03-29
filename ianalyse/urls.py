from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
import settings
from analyse.config import Groups
from analyse import views

urlpatterns = patterns('',
                       url(r'^$',                                     views.home,  name="default"),
                       url(r'^analyse/$',                             views.home,  name="home"),
                       url(r'^analyse/index.html',                    views.index, name="index"),
                       url(r'^analyse/setup.html',                    views.setup, name="setup"),
                       url(r'^analyse/show.html',                     views.show,  name="show"),
                       url(r'^analyse/help.html',                     views.help,  name="help"),                      
                       url(r'^analyse/export.html',                     views.export_as_img,  name="export_as_img"),                        
                       url(r'^analyse/generate.html',                 views.generate, name="generate"),
                       (r'^media/(?P<path>.*)$',                   'django.views.static.serve',
                       {'document_root': settings.MEDIA_ROOT,      'show_indexes': True}),
                       (r'^results/(?P<path>.*)$',                 'django.views.static.serve',
                       {'document_root': Groups().default().results_dir(),   'show_indexes': True})
        )



