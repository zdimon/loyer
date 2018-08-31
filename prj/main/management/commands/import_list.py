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

def getPageList(page):
        
    print 'Downloading %s page' % page

    data = {
    'mode': 'text',
    'com': 'undefined',
    'sort': '3',
    'page': page,
    'text': 'решение суда',
    'swhere': '3',
    'spos': '1',
    'tSynonym': '0',
    'tShort': '1',
    'tSuffix': '1',
    'date': 'undefined',
    'olds': 'undefined',
    'rand': '0.20868381189161633',
    'section': 'jud',
    'tDocsNoClass': '0',
    'excludeArcBuh': '1',
    'status': 'undefined'
    }

    txt = requests.post('https://online.zakon.kz/Search.aspx', data=data, headers=headers).text


    soup = BeautifulSoup(txt, 'html.parser')
    data = []
    for a in soup.find_all('a'):
        try:
            tmp = a.get('id').split('_')
            if len(tmp)==2:
                #print tmp[1]
                data.append({'id':tmp[1],'title': a.getText()})
              
        except Exception, e :
            #print str(e)
            pass
    return data  
    #fn = 'data/pages/%s' % page
    #f = open(fn,'w')
    #f.write(json.dumps(data))
    #f.close() 


def saveItems(d):
    i = Documents()
    i.title = d['title']
    i.uid = d['id']
    i.save()
    print 'Saving %s' % i.uid



class Command(BaseCommand):

    def handle(self, *args, **options):
        print 'Start importing'
        #for page in range(1,5)
        for i in getPageList(3):
            saveItems(i)

