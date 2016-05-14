# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rd', '0005_auto_20160418_2117'),
    ]

    operations = [
        migrations.AddField(
            model_name='detal',
            name='automobile_categories',
            field=models.ManyToManyField(to='rd.CarCategoryDetail', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='detal',
            name='engine_categories',
            field=models.ManyToManyField(to='rd.EngineCategoryDetail', null=True, blank=True),
        ),
    ]
