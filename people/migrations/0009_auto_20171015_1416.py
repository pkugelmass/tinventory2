# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-10-15 18:16
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0008_auto_20171011_2317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='last_login',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2017, 10, 15, 18, 16, 3, 725304, tzinfo=utc), null=True),
        ),
    ]
