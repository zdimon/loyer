# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from bs4 import BeautifulSoup

# Create your models here.
class Documents(models.Model):

    uid = models.IntegerField(default=0, db_index=True)
    title = models.TextField(null=True, blank=True, db_index=True)
    content = models.TextField(null=True, blank=True)
    txt_content = models.TextField(null=True, blank=True)
    is_downloaded = models.BooleanField(default=False)

    def __str__(self):
        return '%s' % (self.id)

    def clearHtml(self):
        print 'Clearing'
        soup = BeautifulSoup(self.content, 'html.parser')   
        d = soup.find("div",{"id": "DocumentText"})
        cleantext = BeautifulSoup(d.text, "lxml").text
        self.txt_content = cleantext
        self.save()
