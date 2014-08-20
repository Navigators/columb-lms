from django.conf.urls import patterns, url
from django.contrib import admin

from lms import lib_view


admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', lib_view.lib_index),
    url(r'^index/$', lib_view.lib_index, name="lib_index"),
    
    url(r'^putaway/$', lib_view.lib_putaway, name="lib_putaway"),
    url(r'^retrieve/$', lib_view.lib_retrieve, name="lib_retrieve"),
    url(r'^booklist/$', lib_view.lib_get_book_list, name="lib_booklist"),
    url(r'^bookinfo/(?P<isbn>\d{13})/$', lib_view.lib_get_book_info, name="lib_bookinfo"),
    url(r'^addcopies/$', lib_view.lib_add_copies, name="lib_addcopies"),
    
    url(r'^buybook/$', lib_view.lib_buybook, name="lib_buybook"),
    
    url(r'^readerinfo/$', lib_view.lib_reader_info, name="lib_readerinfo"),
    
	url(r'^returnborrow/$', lib_view.lib_return_borrow, name="lib_return_borrow"),
	url(r'^borrowpermission/$', lib_view.lib_borrow_permission,name="lib_borrow_permission"),

    
    url(r'^borrowrecord$', lib_view.lib_borrow_record,name="lib_borrow_record"),
    url(r'^overduerecord$', lib_view.lib_overdue,name="lib_overdue_record"),
    
    url(r'^metadata/$', lib_view.lib_meta_data, name="lib_metadata"),
    url(r'^password/$', lib_view.lib_manage_password, name="lib_password"),
    url(r'^pushms/$', lib_view.lib_push_message, name="lib_pushms"),
)
