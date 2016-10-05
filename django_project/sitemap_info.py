#encoding: utf-8
from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse
from rd.models import Detail, CarCategory, EngineCategory
from django.conf import settings
import os


class DetailSitemap(Sitemap):
    priority = 0.64
    def location(self, obj):
        return reverse('detail', args=(obj.url,))

    def items(self):
        return Detail.objects.all()

    def lastmod(self, obj):
        return obj.dm


class EngineSitemap(Sitemap):
    priority = 0.8
    changefreq = 'daily'
    def items(self):
        return EngineCategory.objects.all()


class CarCategorySitemap(Sitemap):
    priority = 0.8
    changefreq = 'daily'
    def items(self):
        return CarCategory.objects.all()


class StaticViewSitemap(Sitemap):
    # priority = 0.8
    changefreq = 'daily'

    def priority(self, item):
        if item == 'index':
            return 1
        else:
            return 0.8

    def items(self):
        return ['index', 'zapchasti', 'price', 'trucks', 'dvigateli', 'about', 'contact']

    def location(self, item):
        return reverse(item)


class PriceExcelSiteMap(Sitemap):
    prefix_path = os.path.join(settings.STATIC_URL, 'upload/price/')
    pdf_file = 'pricelist-cummins-red-diesel.pdf'
    excel_file = 'pricelist-cummins-red-diesel.xls'

    priority = 0.64

    def location(self, obj):
        if obj == 'pdf':
            return os.path.join(self.prefix_path, self.pdf_file)
        if obj == 'excel':
            return os.path.join(self.prefix_path, self.excel_file)

    def items(self):
        return ['pdf', 'excel']