from django.conf.urls import patterns, include, url

from villages.views import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'myfarmreport.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^static/(?P<path>.*)$', views_static_serve),
    url(r'^ajax/register_village/$', register_village),
    url(r'^ajax/get_next_village/$', get_next_village),
)
