# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-07 01:40
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0023_auto_20160407_0636'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Document',
        ),
        migrations.AlterField(
            model_name='art',
            name='dates',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 7, 1, 40, 35, 562825, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='commentform',
            name='dates',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 7, 1, 40, 35, 562367, tzinfo=utc)),
        ),
    ]