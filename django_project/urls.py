# encoding: utf-8
from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.views.generic import TemplateView
import rd.urls
admin.autodiscover()

import django_project.forms
import django_project.views
from django.contrib.sitemaps.views import sitemap
from sitemap_info import DetailSitemap, StaticViewSitemap, PriceExcelSiteMap
urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', TemplateView.as_view(template_name='django_project/index.html'), name='index'),
    url(r'^call-message/$', django_project.views.call_message_view),
    url(r'^json/parts-request/$', django_project.views.parts_request_view),
    url(r'^json/buy-engine/$', django_project.views.buy_engine),
    url(r'^json/question/$', django_project.views.question),
    url(r'^json/detail/$', django_project.views.detail),
    url(r'^json/search_detail/$', django_project.views.search_detail_json),

    #########################################################
    url(r'^zapchasti-cummins/$', TemplateView.as_view(template_name='django_project/zapchasti.html'), name='zapchasti'),
    url(r'^price-cummins/(.*)/$', django_project.views.detail_page, name='detail'),
    url(r'^price-cummins/$', TemplateView.as_view(template_name='django_project/price-cummins.html'), name='price'),
    url(r'^trucks/$', django_project.views.cars, name='trucks'),
    url(r'^trucks/(.*)/$', django_project.views.car_detail, name='trucks_detail'),


    # Передаются сервером
    # url(r'upload/price/pricelist-cummins-red-diesel.pdf')
    # url(r'upload/price/pricelist-cummins-red-diesel.xls')

    # url(r'^zapchasti-cummins/$', django_project.views.engines),
    url(r'^zapchasti-cummins/(.*)/$', django_project.views.engine_detail, name='engines_detail'),

    url(r'^dvigateli-cummins/$', TemplateView.as_view(template_name='django_project/dvigateli.html'), name='dvigateli'),
    url(r'^dvigateli-cummins/isf-2-8/$', TemplateView.as_view(template_name='django_project/isf-2-8.html')),
    url(r'^dvigateli-cummins/isf-3-8/$', TemplateView.as_view(template_name='django_project/isf-3-8.html')),
    url(r'^about/$', TemplateView.as_view(template_name='django_project/about.html'), name='about'),
    url(r'^contact/$', django_project.views.contract, name='contact'),
    url(r'^rd/', include(rd.urls)),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': {'detali': DetailSitemap, 'static': StaticViewSitemap, 'excel': PriceExcelSiteMap}}, name='django.contrib.sitemaps.views.sitemap')
)
