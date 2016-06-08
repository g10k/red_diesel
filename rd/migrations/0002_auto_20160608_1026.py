# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rd', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='carcategory',
            name='about_html',
            field=models.TextField(verbose_name='html', blank=True),
        ),
        migrations.AddField(
            model_name='enginecategory',
            name='about_html',
            field=models.TextField(verbose_name='html', blank=True),
        ),
    ]
