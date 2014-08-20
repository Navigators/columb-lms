from django.conf.urls import patterns, include, url

from django.contrib import admin
from lms import login_view
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', login_view.index),
    url(r'^index/$', login_view.index,name="login"),
    
    url(r'^admin/', include(admin.site.urls)),
    url(r'^rer/', include('lms.rurls',namespace='rer')),
    url(r'^lib/', include('lms.lurls',namespace='lib')),
)
