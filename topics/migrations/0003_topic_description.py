# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-15 17:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0002_topic_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='description',
            field=models.TextField(default='na'),
            preserve_default=False,
        ),
    ]