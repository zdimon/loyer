# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-11 06:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_auto_20180910_1350'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='fact',
            field=models.IntegerField(default=0),
        ),
    ]
