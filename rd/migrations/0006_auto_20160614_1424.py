# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rd', '0005_auto_20160609_0845'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetailCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('sort', models.IntegerField(default=1)),
                ('dc', models.DateTimeField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f')),
                ('dm', models.DateTimeField(auto_now=True, verbose_name='\u041f\u043e\u0441\u043b\u0435\u0434\u043d\u0435\u0435 \u0438\u0437\u043c\u0435\u043d\u0435\u043d\u0438\u0435', db_index=True)),
                ('dd', models.DateTimeField(verbose_name='\u0414\u0430\u0442\u0430 \u0443\u0434\u0430\u043b\u0435\u043d\u0438\u044f', null=True, editable=False, db_index=True)),
                ('related_category', models.ForeignKey(blank=True, to='rd.DetailCategory', null=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': '\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f \u0434\u0435\u0442\u0430\u043b\u0435\u0439',
                'verbose_name_plural': '\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u0438 \u0434\u0435\u0442\u0430\u043b\u0435\u0439',
            },
        ),
        migrations.AddField(
            model_name='detail',
            name='category',
            field=models.ForeignKey(related_name='details', verbose_name='\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f \u0442\u043e\u0432\u0430\u0440\u0430', blank=True, to='rd.DetailCategory', null=True),
        ),
    ]
