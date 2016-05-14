# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rd', '0004_auto_20160415_2124'),
    ]

    operations = [
        migrations.CreateModel(
            name='CarCategoryDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f', blank=True)),
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
            name='CarCategoryDetailPhoto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sort', models.IntegerField(default=1)),
                ('title', models.CharField(max_length=255, verbose_name='\u041f\u043e\u0434\u043f\u0438\u0441\u044c', blank=True)),
                ('image', models.ImageField(upload_to=b'', verbose_name='\u043f\u0443\u0442\u044c \u043a \u043a\u0430\u0440\u0442\u0438\u043d\u043a\u0435')),
                ('category_detal', models.ForeignKey(related_name='photos', to='rd.CarCategoryDetail')),
            ],
            options={
                'ordering': ['sort'],
            },
        ),
        migrations.CreateModel(
            name='EngineCategoryDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f', blank=True)),
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
            name='EngineCategoryDetailPhoto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sort', models.IntegerField(default=1)),
                ('title', models.CharField(max_length=255, verbose_name='\u041f\u043e\u0434\u043f\u0438\u0441\u044c', blank=True)),
                ('image', models.ImageField(upload_to=b'', verbose_name='\u043f\u0443\u0442\u044c \u043a \u043a\u0430\u0440\u0442\u0438\u043d\u043a\u0435')),
                ('category_detal', models.ForeignKey(related_name='photos', to='rd.EngineCategoryDetail')),
            ],
            options={
                'ordering': ['sort'],
            },
        ),
        migrations.AlterModelOptions(
            name='photo',
            options={'ordering': ['sort']},
        ),
        migrations.AddField(
            model_name='photo',
            name='sort',
            field=models.IntegerField(default=1),
        ),
    ]
