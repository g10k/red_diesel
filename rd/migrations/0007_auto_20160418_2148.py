# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rd', '0006_auto_20160418_2122'),
    ]

    operations = [
        migrations.RenameField(
            model_name='detal',
            old_name='inner_id',
            new_name='inner_articul',
        ),
    ]
