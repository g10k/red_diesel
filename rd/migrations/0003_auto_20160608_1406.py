# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('rd', '0002_auto_20160608_1026'),
    ]

    operations = [
        migrations.AddField(
            model_name='carcategory',
            name='dc',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='carcategory',
            name='dd',
            field=models.DateTimeField(verbose_name='\u0414\u0430\u0442\u0430 \u0443\u0434\u0430\u043b\u0435\u043d\u0438\u044f', null=True, editable=False, db_index=True),
        ),
        migrations.AddField(
            model_name='carcategory',
            name='dm',
            field=models.DateTimeField(default=django.utils.timezone.now, auto_now=True, verbose_name='\u041f\u043e\u0441\u043b\u0435\u0434\u043d\u0435\u0435 \u0438\u0437\u043c\u0435\u043d\u0435\u043d\u0438\u0435', db_index=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='detail',
            name='dc',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='detail',
            name='dm',
            field=models.DateTimeField(default=django.utils.timezone.now, auto_now=True, verbose_name='\u041f\u043e\u0441\u043b\u0435\u0434\u043d\u0435\u0435 \u0438\u0437\u043c\u0435\u043d\u0435\u043d\u0438\u0435', db_index=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='enginecategory',
            name='dc',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='enginecategory',
            name='dd',
            field=models.DateTimeField(verbose_name='\u0414\u0430\u0442\u0430 \u0443\u0434\u0430\u043b\u0435\u043d\u0438\u044f', null=True, editable=False, db_index=True),
        ),
        migrations.AddField(
            model_name='enginecategory',
            name='dm',
            field=models.DateTimeField(default=django.utils.timezone.now, auto_now=True, verbose_name='\u041f\u043e\u0441\u043b\u0435\u0434\u043d\u0435\u0435 \u0438\u0437\u043c\u0435\u043d\u0435\u043d\u0438\u0435', db_index=True),
            preserve_default=False,
        ),
    ]
