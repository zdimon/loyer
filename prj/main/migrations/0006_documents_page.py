# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-04 10:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20180904_1008'),
    ]

    operations = [
        migrations.AddField(
            model_name='documents',
            name='page',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
