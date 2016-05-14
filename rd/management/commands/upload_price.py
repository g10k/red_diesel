# coding: utf-8
import datetime

from django.core.management.base import BaseCommand
from django.conf import settings
import sys
import os
import xlwt, xlrd
import rd.models

class Command(BaseCommand):
    help = u"Залить файл в модели, очищает все предыдущее"

    def add_arguments(self, parser):
        parser.add_argument(
            '-f', '--excel_file',
            help='путь до файла',
            action='store',
            required=True
        )

    def set_engine_categories(self, inner_articul, engine_categories_string):
        detail = rd.models.Detal.objects.get(inner_articul=inner_articul)
        detail.engine_categories.all().delete()
        for engine_category_name in engine_categories_string.split(','):
            if not engine_category_name:
                continue
            engine_category,created = rd.models.EngineCategoryDetail.objects.get_or_create(name=engine_category_name)
            detail.engine_categories.add(engine_category)

    def set_car_categories(self, inner_articul, car_categories_string):
        detail = rd.models.Detal.objects.get(inner_articul=inner_articul)
        detail.car_categories.all().delete()
        for car_category_name in car_categories_string.split(','):
            if not car_category_name :
                continue
            car_category, created = rd.models.CarCategoryDetail.objects.get_or_create(name=car_category_name)
            detail.car_categories.add(car_category)



    def handle(self, *args, **options):
        file = options.get('excel_file')
        file_path = os.path.join(settings.BASE_DIR, file)
        rb = xlrd.open_workbook(file_path)
        sheet = rb.sheet_by_index(0)
        if not sheet.nrows:
            return
        rd.models.Detal.objects.all().delete()
        for rownum in range(sheet.nrows):
            row = sheet.row_values(rownum)
            inner_art, articul, name, proizvoditel, engine, auto, cost, nalichie, engine_category, car_category = row[:10]
            if not articul or not name or articul == u'Артикул':
                continue
            try:
                articul = int(articul)
            except:
                pass
            articul = unicode(articul)

            name = unicode(name)
            try:
                cost = unicode(int(round(float(cost))))
            except:
                print cost

            d = rd.models.Detal.objects.create(
                inner_articul=inner_art,
                articul=articul,
                name=name,
                cost=cost,
                proizvoditel=proizvoditel,
                engine=engine,
                automobile=auto,
                nalichie=nalichie
            )
            d.url = d.get_absolute_url()
            d.save()

            self.set_engine_categories(d.inner_articul, engine_category)
            self.set_car_categories(d.inner_articul, car_category)