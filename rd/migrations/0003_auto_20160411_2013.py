# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rd', '0002_detal_test'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detal',
            name='related_details',
            field=models.ManyToManyField(to='rd.Detal', null=True, verbose_name='\u0421\u0432\u044f\u0437\u0430\u043d\u043d\u044b\u0435 \u0434\u0435\u0442\u0430\u043b\u0438'),
        ),
    ]
