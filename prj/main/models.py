# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from bs4 import BeautifulSoup

# Create your models here.

class Log(models.Model):
    date = models.DateField(unique=True)
    cnt = models.IntegerField(default=0, null=True, blank=True)
    fact = models.IntegerField(default=0)

    def update(self):
        cnt = Documents.objects.filter(date=self.date).count()
        self.fact = cnt
        self.save()

class Documents(models.Model):

    uid = models.CharField(max_length=250, db_index=True)
    title = models.TextField(null=True, blank=True, db_index=True)
    is_file_downloaded = models.BooleanField(default=False)
    href = models.CharField(max_length=250, null=True, blank=True)
    date = models.DateField(null=True, blank=True, db_index=True)
    is_error = models.BooleanField(default=False)
    is_document_downloaded = models.BooleanField(default=False)
    is_files_downloaded = models.BooleanField(default=False)
    doc_html = models.TextField(null=True, blank=True)
    doc_txt = models.TextField(null=True, blank=True)
    
    def check_document(self):
        #print 'Checking'
        #soup = BeautifulSoup(self.doc_html, 'html.parser') 
        #try:
        #h2 = soup.find('h2')
        #print h2
        print len(self.doc_html)
    
    @property
    def txt(self):
        
        
        try:
            doc = DocumentContent.objects.get(document=self)
            return doc.cleanText
        except:
            return 'не скачено'

    def __str__(self):
        return '%s' % (self.id)

    def clearDocHtml(self):
        print 'Clearing'
        result = False
        try:
            soup = BeautifulSoup(self.doc_html, 'html.parser')   
            d = soup.find("div",{"class": "contents"})
            cleantext = BeautifulSoup(d.text, "lxml").text
            self.doc_txt = cleantext
            self.is_document_downloaded = True
            result = True
        except:
            self.is_document_downloaded = False
        self.save()
        return result
        





class Files(models.Model):

    document = models.ForeignKey(Documents, null=True, blank=True)
    html = models.TextField(null=True, blank=True)
    url = models.CharField(max_length=250, null=True, blank=True)
    txt = models.TextField(null=True, blank=True)
    is_error = models.BooleanField(default=False)
    is_downloaded = models.BooleanField(default=False)
    def clearHtml(self):
        print 'Clearing'
        try:
            soup = BeautifulSoup(self.html, 'html.parser')   
            d = soup.find("div",{"class": "docblock"})
            cleantext = BeautifulSoup(d.text, "lxml").text
            self.txt = cleantext
        except:
            pass
        self.save()


    #@property
    #def cleanText(self):
    #    return self.txt.replace('< Вернуться к результатам','')
