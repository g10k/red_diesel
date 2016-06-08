# encoding: utf-8
from django.conf.urls import patterns, url

import rd.views

urlpatterns = patterns('',
    url(r'^excel/main/$', rd.views.excel_upload),
    url(r'^update_urls/$', rd.views.update_urls),
)