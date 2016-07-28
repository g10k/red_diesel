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
    url(r'^zapchasti-cummins/(.*)/$', django_project.views.detail_page, name='engines_detail'),

    url(r'^dvigateli-cummins/$', TemplateView.as_view(template_name='django_project/dvigateli.html'), name='dvigateli'),
    url(r'^dvigateli-cummins/isf-2-8/$', TemplateView.as_view(template_name='django_project/isf-2-8.html')),
    url(r'^dvigateli-cummins/isf-3-8/$', TemplateView.as_view(template_name='django_project/isf-3-8.html')),
    url(r'^dvigateli-cummins/4isbe/$', TemplateView.as_view(template_name='django_project/4isbe.html')),
    url(r'^dvigateli-cummins/6isbe/$', TemplateView.as_view(template_name='django_project/6isbe.html')),
    url(r'^dvigateli-cummins/4bt/$', TemplateView.as_view(template_name='django_project/4bt.html')),
    url(r'^dvigateli-cummins/6bt/$', TemplateView.as_view(template_name='django_project/6bt.html')),
    url(r'^dvigateli-cummins/eqb/$', TemplateView.as_view(template_name='django_project/eqb.html')),
    url(r'^dvigateli-cummins/qsb/$', TemplateView.as_view(template_name='django_project/qsb.html')),
    url(r'^dvigateli-cummins/6ct/$', TemplateView.as_view(template_name='django_project/6ct.html')),
    url(r'^dvigateli-cummins/qsc/$', TemplateView.as_view(template_name='django_project/qsc.html')),
    url(r'^dvigateli-cummins/isc/$', TemplateView.as_view(template_name='django_project/isc.html')),
    url(r'^dvigateli-cummins/l/$', TemplateView.as_view(template_name='django_project/l.html')),
    url(r'^dvigateli-cummins/isle/$', TemplateView.as_view(template_name='django_project/isle.html')),
    url(r'^dvigateli-cummins/qsl/$', TemplateView.as_view(template_name='django_project/qsl.html')),
    url(r'^dvigateli-cummins/m11/$', TemplateView.as_view(template_name='django_project/m11.html')),
    url(r'^dvigateli-cummins/qsm/$', TemplateView.as_view(template_name='django_project/qsm.html')),
    url(r'^dvigateli-cummins/isme/$', TemplateView.as_view(template_name='django_project/isme.html')),
    url(r'^dvigateli-cummins/isx/$', TemplateView.as_view(template_name='django_project/isx.html')),
    url(r'^dvigateli-cummins/qsx/$', TemplateView.as_view(template_name='django_project/qsx.html')),
    url(r'^dvigateli-cummins/k19/$', TemplateView.as_view(template_name='django_project/k19.html')),
    url(r'^dvigateli-cummins/qsk19/$', TemplateView.as_view(template_name='django_project/qsk19.html')),
    url(r'^dvigateli-cummins/a/$', TemplateView.as_view(template_name='django_project/a.html')),
    url(r'^dvigateli-cummins/isf-2-8-test/$', TemplateView.as_view(template_name='django_project/isf-2-8-test.html')),
    url(r'^about/$', TemplateView.as_view(template_name='django_project/about.html'), name='about'),
    url(r'^contact/$', django_project.views.contract, name='contact'),
    url(r'^rd/', include(rd.urls)),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': {'detali': DetailSitemap, 'static': StaticViewSitemap, 'excel': PriceExcelSiteMap}}, name='django.contrib.sitemaps.views.sitemap')
)
