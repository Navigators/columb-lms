from django.conf.urls import patterns, include, url
from django.contrib import admin
from lms import views
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'columb.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', views.lms_index,name="index"),
    url(r'^addbook$', views.lms_addbook,name="addbook"),
)
