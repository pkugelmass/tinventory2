# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-21 02:46
from __future__ import unicode_literals

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0011_auto_20170820_1035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resource',
            name='slug',
            field=autoslug.fields.AutoSlugField(always_update=True, editable=False, populate_from='title', unique=True),
        ),
    ]
