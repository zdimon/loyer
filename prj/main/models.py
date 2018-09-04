# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from bs4 import BeautifulSoup

# Create your models here.
class Documents(models.Model):

    uid = models.CharField(max_length=250, db_index=True, unique=True)
    title = models.TextField(null=True, blank=True, db_index=True)
    content = models.TextField(null=True, blank=True)
    txt_content = models.TextField(null=True, blank=True)
    is_downloaded = models.BooleanField(default=False)
    href = models.CharField(max_length=250, null=True, blank=True)
    page = models.IntegerField(default=0, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    is_error = models.BooleanField(default=False)

    def __str__(self):
        return '%s' % (self.id)

    def clearHtml(self):
        print 'Clearing'
        soup = BeautifulSoup(self.content, 'html.parser')   
        d = soup.find("div",{"id": "DocumentText"})
        cleantext = BeautifulSoup(d.text, "lxml").text
        self.txt_content = cleantext
        self.save()
        
class DocumentContent(models.Model):
    TYPES = (
        ('Not Found', 'Not Found'),
        ('Not registered', 'Not registered')
    )

    document = models.ForeignKey(Documents, on_delete=models.CASCADE)
    html = models.TextField(null=True, blank=True)
    txt = models.TextField(null=True, blank=True)
    length =  models.IntegerField(null=True, blank=True)
    is_error = models.BooleanField(default=False)
    type_error = models.CharField(max_length = 20, db_index=True, choices=TYPES, null=True, blank=True)

    def checkErrors(self):
         if self.txt.find('Дело не найдено')>0:
            self.is_error = True
            self.type_error = 'Not Found'
            self.save()

    def clearHtml(self):
        #print 'Clearing'
        soup = BeautifulSoup(self.html, 'html.parser')   
        d = soup.find("div",{"class": "grayblock"})
        try:
            cleantext = BeautifulSoup(d.text, "lxml").text
        except Exception, e:
            cleantext = str(e)
            self.is_error = True
        self.txt = cleantext
        self.save()
