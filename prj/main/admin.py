# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from main.models import Documents
# Register your models here.

class DocumentsAdmin(admin.ModelAdmin):
    list_display = ('uid', 'title', 'is_downloaded')
admin.site.register(Documents, DocumentsAdmin)

