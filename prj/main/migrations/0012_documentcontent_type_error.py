# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-04 13:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20180904_1258'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentcontent',
            name='type_error',
            field=models.CharField(blank=True, choices=[('Not Found', 'Not Found'), ('Not registered', 'Not registered')], db_index=True, max_length=2, null=True),
        ),
    ]