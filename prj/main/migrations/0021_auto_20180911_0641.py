# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-11 06:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_log_fact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='cnt',
            field=models.IntegerField(blank=True, default=0, max_length=25, null=True),
        ),
    ]
