from django.conf.urls import patterns, url
from django.contrib import admin

from lms import rer_view


admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', rer_view.reader_index, name="reader_index"),
    url(r'^index/$', rer_view.reader_index, name="reader_index"),
    
    url(r'^loan/$', rer_view.reader_loan, name="reader_loan"),
    url(r'^point/$', rer_view.reader_point, name="reader_point"),
    url(r'^profile/$', rer_view.reader_profile, name="reader_profile"),
    url(r'^review/$', rer_view.reader_review, name="reader_review"),
    
    url(r'^buybook/$', rer_view.reader_buy_book, name="reader_buy_book"),
    
    url(r'^bookdetails/(?P<book_id>\d+)$', rer_view.reader_book_detail, name="reader_book_detail"),
)
