# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rd', '0007_auto_20160418_2148'),
    ]

    operations = [
        migrations.RenameField(
            model_name='detal',
            old_name='automobile_categories',
            new_name='car_categories',
        ),
    ]
