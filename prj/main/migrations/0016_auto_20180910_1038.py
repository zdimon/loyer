# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-10 10:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_auto_20180910_0836'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='documents',
            name='content',
        ),
        migrations.RemoveField(
            model_name='documents',
            name='is_downloaded',
        ),
        migrations.RemoveField(
            model_name='documents',
            name='list_html',
        ),
        migrations.RemoveField(
            model_name='documents',
            name='list_txt',
        ),
        migrations.RemoveField(
            model_name='documents',
            name='txt_content',
        ),
        migrations.AlterField(
            model_name='documents',
            name='date',
            field=models.DateField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='log',
            name='date',
            field=models.DateField(unique=True),
        ),
    ]
