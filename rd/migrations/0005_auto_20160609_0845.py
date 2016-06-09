# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rd', '0004_auto_20160609_0840'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='carcategory',
            options={'ordering': ['-sort'], 'verbose_name': '\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f \u043c\u0430\u0448\u0438\u043d\u044b', 'verbose_name_plural': '\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u0438 \u043c\u0430\u0448\u0438\u043d\u044b'},
        ),
        migrations.AlterModelOptions(
            name='carcategoryphoto',
            options={'ordering': ['-sort']},
        ),
        migrations.AlterModelOptions(
            name='enginecategory',
            options={'ordering': ['-sort'], 'verbose_name': '\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f \u0434\u0432\u0438\u0433\u0430\u0442\u0435\u043b\u044f', 'verbose_name_plural': '\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u0438 \u0434\u0432\u0438\u0433\u0430\u0442\u0435\u043b\u0435\u0439'},
        ),
        migrations.AlterModelOptions(
            name='enginecategoryphoto',
            options={'ordering': ['-sort']},
        ),
        migrations.AlterModelOptions(
            name='photo',
            options={'ordering': ['-sort']},
        ),
    ]
