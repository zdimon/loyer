# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-04 12:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_documentcontent_length'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentcontent',
            name='txt',
            field=models.TextField(blank=True, null=True),
        ),
    ]