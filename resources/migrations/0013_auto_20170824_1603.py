# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-24 20:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0012_auto_20170820_2246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resource',
            name='title',
            field=models.CharField(max_length=80, verbose_name='Title'),
        ),
    ]