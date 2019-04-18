# -*- coding: utf-8 -*-
#http://office.sud.kz/courtActs/site/lawsuitList.xhtml
from django.core.management.base import BaseCommand, CommandError
import json
from prj.settings import BASE_DIR
import os
from main.models import *
import requests
from bs4 import BeautifulSoup
import os.path
import time
import json
from main.tools import headers


class Command(BaseCommand):

    def handle(self, *args, **options):
        print 'Start looping'
       
        for d in Documents.objects.filter(is_document_downloaded=True):
            print 'Process %s' % d.id
            d.check_document()
        '''       
        for d in Log.objects.all().order_by('id'):
            print 'Processing %s' % d.id
            #d.cnt = d.cnt.replace(' ','')
            cnt = Documents.objects.filter(date=d.date).count()
            d.fact = cnt
            d.save()
            #d.clearDocHtml()
        
            try: 
                dd = DocumentContent.objects.get(document=d)
                d.doc_html = dd.html
                d.is_document_downloaded = True
                d.save()
                d.clearHtml()
                print 'Done!'
            except:
                print 'Not exist!'
            '''
            #d.clearDocHtml()
            #d.clearListHtml()
        #getSessionId()

