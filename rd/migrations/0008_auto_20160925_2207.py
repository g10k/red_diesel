# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import csv
# from django.conf import settings
import os


def load_cities(apps, schema_editor):
    City = apps.get_model('rd', 'City')
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'cities.csv'), 'rb') as f:
        r = csv.reader(f, delimiter=' '.encode('utf8'))
        cities = [row for row in r]
        for city in cities:
            City.objects.create(en_name=city[0], ru_name=city[1].decode('utf8'))

class Migration(migrations.Migration):

    dependencies = [
        ('rd', '0007_auto_20160925_2153'),
    ]

    operations = [
        migrations.RunPython(load_cities),
    ]
