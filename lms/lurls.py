from django.conf.urls import patterns,url
from django.contrib import admin

from lms import views


admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'columb.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
#     url(r'^$', views.read_index,name="read_index"),

    url(r'^$', views.lib_index),
    url(r'^index/$', views.lib_index,name="lib_index"),
    
    url(r'^putaway/$', views.lib_putaway,name="lib_putaway"),
    url(r'^retrieve/$', views.lib_retrieve,name="lib_retrieve"),
    url(r'^booklist/$', views.lib_get_book_list,name="lib_booklist"),
    url(r'^bookinfo/(?P<isbn>\d{13})/$', views.lib_get_book_info,name="lib_bookinfo"),
    url(r'^addcopies/$', views.lib_add_copies,name="lib_addcopies"),
    
    
    url(r'^buybook/$', views.lib_buybook,name="lib_buybook"),

	url(r'^returnborrow$', views.lib_return_borrow,name="lib_return_borrow"),
)
