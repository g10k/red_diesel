# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rd', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='detal',
            name='test',
            field=models.TextField(verbose_name='\u0422\u0435\u043a\u0441\u0442', blank=True),
        ),
    ]
