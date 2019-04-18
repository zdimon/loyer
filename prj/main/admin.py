# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from main.models import *
# Register your models here.

class DocumentsAdmin(admin.ModelAdmin):
    list_display = ('uid', 'date', 'title', 'is_document_downloaded',  'doc_txt')
    #list_filter = ('is_error', 'is_document_downloaded', 'date', 'id')
    list_filter = ('is_document_downloaded',)
    search_fields = ('uid', 'date')
    ordering = ('-id',)
admin.site.register(Documents, DocumentsAdmin)




class FilesAdmin(admin.ModelAdmin):
    list_display = ('id','document', 'txt', 'is_error')
    list_filter = ('is_error',)
    ordering = ('-id',)
admin.site.register(Files, FilesAdmin)


class LogAdmin(admin.ModelAdmin):
    list_display = ('date','cnt', 'fact')
    ordering = ('-date',)
admin.site.register(Log, LogAdmin)
