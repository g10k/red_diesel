# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CarCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.CharField(max_length=400, verbose_name='\u0420\u0443\u0447\u043d\u043e\u0439 url', blank=True)),
                ('name', models.CharField(max_length=255, verbose_name='\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f')),
                ('title', models.CharField(max_length=255, verbose_name='title', blank=True)),
                ('description', models.CharField(max_length=255, verbose_name='description', blank=True)),
                ('keywords', models.CharField(max_length=255, verbose_name='keywords', blank=True)),
                ('header', models.CharField(max_length=255, verbose_name='heading', blank=True)),
            ],
            options={
                'verbose_name': '\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f \u043c\u0430\u0448\u0438\u043d\u044b',
            },
        ),
        migrations.CreateModel(
            name='CarCategoryPhoto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sort', models.IntegerField(default=1)),
                ('title', models.CharField(max_length=255, verbose_name='\u041f\u043e\u0434\u043f\u0438\u0441\u044c', blank=True)),
                ('image', models.ImageField(upload_to=b'car-categories/', verbose_name='\u043f\u0443\u0442\u044c \u043a \u043a\u0430\u0440\u0442\u0438\u043d\u043a\u0435')),
                ('category_detal', models.ForeignKey(related_name='photos', to='rd.CarCategory')),
            ],
            options={
                'ordering': ['sort'],
            },
        ),
        migrations.CreateModel(
            name='Detail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('inner_articul', models.CharField(max_length=255, verbose_name='\u0412\u043d\u0443\u0442\u0440\u0435\u043d\u043d\u0438\u0439 \u0430\u0440\u0442\u0438\u043a\u0443\u043b')),
                ('articul', models.CharField(max_length=255, verbose_name='\u0410\u0440\u0442\u0438\u043a\u0443\u043b', db_index=True)),
                ('name', models.TextField(verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('cost', models.CharField(max_length=255, verbose_name='\u0426\u0435\u043d\u0430')),
                ('test', models.TextField(verbose_name='\u0422\u0435\u043a\u0441\u0442', blank=True)),
                ('nalichie', models.CharField(max_length=255, verbose_name='\u041d\u0430\u043b\u0438\u0447\u0438\u0435', blank=True)),
                ('proizvoditel', models.CharField(max_length=255, verbose_name='\u041f\u0440\u043e\u0438\u0437\u0432\u043e\u0434\u0438\u0442\u0435\u043b\u044c', blank=True)),
                ('engine', models.CharField(max_length=255, verbose_name='\u0414\u0432\u0438\u0433\u0430\u0442\u0435\u043b\u044c', blank=True)),
                ('automobile', models.CharField(max_length=255, verbose_name='\u0410\u0432\u0442\u043e\u043c\u043e\u0431\u0438\u043b\u044c', blank=True)),
                ('old_url', models.CharField(max_length=400, verbose_name='\u0421\u0442\u0430\u0440\u044b\u0439 url', blank=True)),
                ('url', models.CharField(max_length=400, verbose_name='\u0420\u0443\u0447\u043d\u043e\u0439 url')),
                ('title', models.CharField(max_length=255, verbose_name='title', blank=True)),
                ('description', models.CharField(max_length=255, verbose_name='description', blank=True)),
                ('header', models.CharField(max_length=255, verbose_name='\u0437\u0430\u0433\u043e\u043b\u043e\u0432\u043e\u043a', blank=True)),
                ('dd', models.DateTimeField(verbose_name='\u0414\u0430\u0442\u0430 \u0443\u0434\u0430\u043b\u0435\u043d\u0438\u044f', null=True, editable=False, db_index=True)),
                ('cars', models.ManyToManyField(to='rd.CarCategory', null=True, blank=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': '\u0414\u0435\u0442\u0430\u043b\u044c',
                'verbose_name_plural': '\u0414\u0435\u0442\u0430\u043b\u044c',
            },
        ),
        migrations.CreateModel(
            name='EngineCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.CharField(max_length=400, verbose_name='\u0420\u0443\u0447\u043d\u043e\u0439 url', blank=True)),
                ('name', models.CharField(max_length=255, verbose_name='\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f')),
                ('title', models.CharField(max_length=255, verbose_name='title', blank=True)),
                ('description', models.CharField(max_length=255, verbose_name='description', blank=True)),
                ('keywords', models.CharField(max_length=255, verbose_name='keywords', blank=True)),
                ('header', models.CharField(max_length=255, verbose_name='heading', blank=True)),
            ],
            options={
                'verbose_name': '\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f \u0434\u0432\u0438\u0433\u0430\u0442\u0435\u043b\u044f',
            },
        ),
        migrations.CreateModel(
            name='EngineCategoryPhoto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sort', models.IntegerField(default=1)),
                ('title', models.CharField(max_length=255, verbose_name='\u041f\u043e\u0434\u043f\u0438\u0441\u044c', blank=True)),
                ('image', models.ImageField(upload_to=b'dvigateli-cummins/', verbose_name='\u043f\u0443\u0442\u044c \u043a \u043a\u0430\u0440\u0442\u0438\u043d\u043a\u0435')),
                ('category_detal', models.ForeignKey(related_name='photos', to='rd.EngineCategory')),
            ],
            options={
                'ordering': ['sort'],
            },
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sort', models.IntegerField(default=1)),
                ('title', models.CharField(max_length=255, verbose_name='\u041f\u043e\u0434\u043f\u0438\u0441\u044c', blank=True)),
                ('image', models.ImageField(upload_to=b'', verbose_name='\u043f\u0443\u0442\u044c \u043a \u043a\u0430\u0440\u0442\u0438\u043d\u043a\u0435')),
                ('detal', models.ForeignKey(related_name='photos', to='rd.Detail')),
            ],
            options={
                'ordering': ['sort'],
            },
        ),
        migrations.AddField(
            model_name='detail',
            name='engines',
            field=models.ManyToManyField(to='rd.EngineCategory', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='detail',
            name='related_details',
            field=models.ManyToManyField(to='rd.Detail', null=True, verbose_name='\u0421\u0432\u044f\u0437\u0430\u043d\u043d\u044b\u0435 \u0434\u0435\u0442\u0430\u043b\u0438', blank=True),
        ),
    ]
