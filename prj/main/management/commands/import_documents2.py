# -*- coding: utf-8 -*-
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
from main.tools import getSessionId, readSessionId, getSessionId, readPHPSessionId
import sys
import os



def processDoc(limit):
    docs = Documents.objects.filter(is_downloaded=False).order_by('id')[0:limit]
    for d in docs:
        #print d.id
        s = requests.Session()
        ses =  readSessionId()
        phpsessid = readPHPSessionId()
        cookies = {'PHPSESSID': phpsessid, 'SessionId':  ses}
        url = 'http://online.zakon.kz/sud//'+d.href
        print 'processing %s for %s' % (d.id, d.date)
        txt = s.get(url,headers=headers,cookies=cookies).text
        c = DocumentContent()
        c.html = txt
        c.document = d
        c.length = len(txt)
        c.clearHtml()
        c.checkErrors()
        c.save()
        d.is_downloaded = True
        d.save()
        
       
        
        
        #break
    #return True
        #
    time.sleep(2)
    processDoc(limit)

                          
class Command(BaseCommand):

    def handle(self, *args, **options):
        print 'Start importing documents'
        processDoc(100)
        
       
