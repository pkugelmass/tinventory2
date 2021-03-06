# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-09-08 01:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0013_auto_20170824_1603'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('resources.resource',),
        ),
        migrations.AddField(
            model_name='resource',
            name='post',
            field=models.TextField(blank=True, help_text='Type your post here.', null=True, verbose_name='Post'),
        ),
        migrations.AlterField(
            model_name='resource',
            name='type',
            field=models.CharField(choices=[('file', 'File'), ('link', 'Link'), ('post', 'Post')], max_length=5, verbose_name='Resource Type'),
        ),
    ]
