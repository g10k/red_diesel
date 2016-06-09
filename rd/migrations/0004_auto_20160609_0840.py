# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rd', '0003_auto_20160608_1406'),
    ]

    operations = [
        migrations.AddField(
            model_name='carcategory',
            name='sort',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='detail',
            name='sort',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='enginecategory',
            name='sort',
            field=models.IntegerField(default=1),
        ),
    ]
