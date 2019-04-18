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
import random
from datetime import datetime, timedelta
from optparse import make_option
from header import copy_cookie, copy_header

def randomDelay():
    sl = random.randint(10,20)
    print 'sleeping %s' % sl
    time.sleep(sl)




def makeRequest(url):
    try:
        txt = requests.get(url,headers=copy_header,cookies=copy_cookie).text     
        return txt       
    except requests.exceptions.ReadTimeout as errh:
        print ("Http Error timeout!")    

def checkHtml(html):
    return True

def saveDoc(l):
    print 'Saving %s for %s' % (l.id,l.date)
    url = 'http://online.zakon.kz/sud/'+l.href
    txt = makeRequest(url)
    if checkHtml(txt):
        l.doc_html = txt
        l.clearDocHtml()
    randomDelay()
    
cnt = 0

def process(lst=None):
    global cnt
    if lst==None:
        lst = Documents.objects.filter(is_document_downloaded=False).order_by('-date')[0:10]
    for l in lst:
        res = saveDoc(l)
        cnt = cnt + 1
        print 'Count - %s' % cnt
        if res == False:
            sys.exit('Error parsing!!!!')
    lst = Documents.objects.filter(is_document_downloaded=False).order_by('-date')[0:10]
    process(lst)






class Command(BaseCommand):


    def handle(self, *args, **options):
        
        print 'Start process'
        process()
       
