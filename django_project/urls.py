# encoding: utf-8
from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.views.generic import TemplateView
import rd.urls
admin.autodiscover()

import django_project.forms
import django_project.views

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', TemplateView.as_view(template_name='rd/index.html')),
    url(r'^call-message/$', django_project.views.call_message_view),
    url(r'^json/parts-request/$', django_project.views.parts_request_view),
    url(r'^json/buy-engine/$', django_project.views.buy_engine),
    url(r'^json/question/$', django_project.views.question),
    url(r'^json/detail/$', django_project.views.detail),
    url(r'^zapchasti-cummins/$', TemplateView.as_view(template_name='rd/zapchasti.html')),
    url(r'^zapchasti-cummins/(.*)/$', django_project.views.detail_page),
    url(r'^price-cummins/$', TemplateView.as_view(template_name='rd/price-cummins.html')),
    url(r'^car_categories/$', django_project.views.cars),
    url(r'^dvigateli-cummins/$', TemplateView.as_view(template_name='rd/dvigateli.html')),
    url(r'^detail-page-test/$', TemplateView.as_view(template_name='rd/detail_page_test.html')),
    url(r'^dvigateli-cummins/isf-2-8/$', TemplateView.as_view(template_name='rd/isf-2-8.html')),
    url(r'^dvigateli-cummins/isf-3-8/$', TemplateView.as_view(template_name='rd/isf-3-8.html')),
    url(r'^about/$', TemplateView.as_view(template_name='rd/about.html')),
    url(r'^contact/$', django_project.views.contract),
    url(r'^rd/', include(rd.urls)),
)
