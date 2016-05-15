# encoding: utf-8
from django.conf.urls import patterns, url

import rd.views

urlpatterns = patterns('',
    url(r'excel_upload/$', rd.views.excel_upload),
)