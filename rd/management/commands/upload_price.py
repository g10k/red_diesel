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

    def set_engines(self, inner_articul, engines_string):
        detail = rd.models.Detail.objects.get(inner_articul=inner_articul)
        detail.engines.all().delete()
        for engine_category_name in engines_string.split(','):
            if not engine_category_name:
                continue
            engine_category,created = rd.models.EngineCategory.objects.get_or_create(name=engine_category_name)
            detail.engines.add(engine_category)

    def set_car_categories(self, inner_articul, cars_string):
        detail = rd.models.Detail.objects.get(inner_articul=inner_articul)
        detail.cars.all().delete()
        for car_category_name in cars_string.split(','):
            if not car_category_name :
                continue
            car_category, created = rd.models.CarCategory.objects.get_or_create(name=car_category_name)
            detail.cars.add(car_category)

    def handle(self, *args, **options):
        file = options.get('excel_file')
        file_path = os.path.join(settings.BASE_DIR, file)
        rb = xlrd.open_workbook(file_path)
        sheet = rb.sheet_by_index(0)
        if not sheet.nrows:
            return
        rd.models.Detail.objects.all().delete()
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

            d = rd.models.Detail.objects.create(
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

            self.set_engines(d.inner_articul, engine_category)
            self.set_car_categories(d.inner_articul, car_category)