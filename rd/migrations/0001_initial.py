# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Detal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('articul', models.CharField(max_length=255, verbose_name='\u0410\u0440\u0442\u0438\u043a\u0443\u043b', db_index=True)),
                ('name', models.TextField(verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('cost', models.CharField(max_length=255, verbose_name='\u0426\u0435\u043d\u0430')),
                ('nalichie', models.CharField(max_length=255, verbose_name='\u041d\u0430\u043b\u0438\u0447\u0438\u0435', blank=True)),
                ('proizvoditel', models.CharField(max_length=255, verbose_name='\u041f\u0440\u043e\u0438\u0437\u0432\u043e\u0434\u0438\u0442\u0435\u043b\u044c', blank=True)),
                ('engine', models.CharField(max_length=255, verbose_name='\u0414\u0432\u0438\u0433\u0430\u0442\u0435\u043b\u044c', blank=True)),
                ('automobile', models.CharField(max_length=255, verbose_name='\u0410\u0432\u0442\u043e\u043c\u043e\u0431\u0438\u043b\u044c', blank=True)),
                ('url', models.CharField(max_length=400, verbose_name='\u0420\u0443\u0447\u043d\u043e\u0439 url')),
                ('related_details', models.ManyToManyField(to='rd.Detal', verbose_name='\u0421\u0432\u044f\u0437\u0430\u043d\u043d\u044b\u0435 \u0434\u0435\u0442\u0430\u043b\u0438')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': '\u0414\u0435\u0442\u0430\u043b\u044c',
                'verbose_name_plural': '\u0414\u0435\u0442\u0430\u043b\u044c',
            },
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='\u041f\u043e\u0434\u043f\u0438\u0441\u044c', blank=True)),
                ('image', models.ImageField(upload_to=b'', verbose_name='\u043f\u0443\u0442\u044c \u043a \u043a\u0430\u0440\u0442\u0438\u043d\u043a\u0435')),
                ('detal', models.ForeignKey(related_name='photos', to='rd.Detal')),
            ],
        ),
    ]
