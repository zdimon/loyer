# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from main.models import Documents, DocumentContent
# Register your models here.

class DocumentsAdmin(admin.ModelAdmin):
    list_display = ('uid', 'date','title', 'is_downloaded', 'page', 'href')
    list_filter = ('is_error', 'is_downloaded')
    ordering = ('-id',)
admin.site.register(Documents, DocumentsAdmin)


class DocumentContentAdmin(admin.ModelAdmin):
    list_display = ('id','document', 'is_error', 'txt')
    list_filter = ('is_error',)
    ordering = ('-id',)
admin.site.register(DocumentContent, DocumentContentAdmin)


