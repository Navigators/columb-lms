from django.conf.urls import patterns,url
from django.contrib import admin

from lms import views


admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'columb.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
#     url(r'^$', views.read_index,name="read_index"),

    url(r'^$', views.reader_index,name="reader_index"),
    url(r'^index/$', views.reader_index,name="reader_index"),
)