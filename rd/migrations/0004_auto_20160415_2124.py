# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rd', '0003_auto_20160411_2013'),
    ]

    operations = [
        migrations.AddField(
            model_name='detal',
            name='description',
            field=models.CharField(max_length=255, verbose_name='description', blank=True),
        ),
        migrations.AddField(
            model_name='detal',
            name='header',
            field=models.CharField(max_length=255, verbose_name='\u0437\u0430\u0433\u043e\u043b\u043e\u0432\u043e\u043a', blank=True),
        ),
        migrations.AddField(
            model_name='detal',
            name='inner_id',
            field=models.CharField(default='nn', max_length=255, verbose_name='\u0412\u043d\u0443\u0442\u0440\u0435\u043d\u043d\u0438\u0439 \u0430\u0440\u0442\u0438\u043a\u0443\u043b'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='detal',
            name='title',
            field=models.CharField(max_length=255, verbose_name='title', blank=True),
        ),
        migrations.AlterField(
            model_name='detal',
            name='related_details',
            field=models.ManyToManyField(to='rd.Detal', null=True, verbose_name='\u0421\u0432\u044f\u0437\u0430\u043d\u043d\u044b\u0435 \u0434\u0435\u0442\u0430\u043b\u0438', blank=True),
        ),
    ]
