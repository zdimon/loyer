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

'''
j_idt9: j_idt9
javax.faces.ViewState: -533918060567300745:-2199755061829682293
javax.faces.source: j_idt9:j_idt21:1:j_idt24
javax.faces.partial.event: click
javax.faces.partial.execute: j_idt9:j_idt21:1:j_idt24 @component
javax.faces.partial.render: @component
thisPage: 2
org.richfaces.ajax.component: j_idt9:j_idt21:1:j_idt24
j_idt9:j_idt21:1:j_idt24: j_idt9:j_idt21:1:j_idt24
rfExt: null
AJAX:EVENTS_COUNT: 1
javax.faces.partial.ajax: true


j_idt9: j_idt9
javax.faces.ViewState: -3744060389296387497:-5940256457322138936
javax.faces.source: j_idt9:j_idt21:1:j_idt24
javax.faces.partial.event: click
javax.faces.partial.execute: j_idt9:j_idt21:1:j_idt24 @component
javax.faces.partial.render: @component
thisPage: 2
org.richfaces.ajax.component: j_idt9:j_idt21:1:j_idt24
j_idt9:j_idt21:1:j_idt24: j_idt9:j_idt21:1:j_idt24
rfExt: null
AJAX:EVENTS_COUNT: 1
javax.faces.partial.ajax: true




j_idt17: j_idt17
j_idt17:edit-period: 2018
j_idt17:edit-period-hide: 
j_idt17:edit-participantTypeCheckbox: FIRSTINSTANCE
j_idt17:edit-participantTypeCheckbox: APPEAL
j_idt17:edit-participant: 
j_idt17:edit-dateFrom: 01.01.2018
j_idt17:edit-dateFrom-hid: 01.01.2018
j_idt17:edit-dateTo: 31.12.2018
j_idt17:edit-dateTo-hid: 31.12.2018
j_idt17:edit-category: 
j_idt17:edit-district: 2
j_idt17:edit-court: 
j_idt17:iinOrBin: 
j_idt17:plaintff: 
j_idt17:defendant: 
j_idt17:attorney: 
j_idt17:edit-consideration: 


'''

headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Length': '931',
    'Content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
    'Faces-Request': 'partial/ajax',
    'Host': 'office.sud.kz',
    'Origin': 'http://office.sud.kz',
    'Pragma': 'no-cache',
    'Referer': 'http://office.sud.kz/courtActs/site/index.xhtml?l=rus',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36'
}

class Command(BaseCommand):

    def handle(self, *args, **options):
        print 'Start'
        s = requests.Session()
        url = 'http://office.sud.kz/courtActs/site/lawsuitList.xhtml'


        r = s.get('http://office.sud.kz/courtActs/site/index.xhtml?l=rus')
       
        session_id = r.cookies.get_dict()['JSESSIONID']
        print session_id

        my_cookies = {'JSESSIONID': session_id, 'COURTSERVERID':'court2'}
        
        data = {
            'j_idt17': 'j_idt17',
            'j_idt17%3Aedit-period: ': '2018',
            'j_idt17%3Aedit-period-hide': '',
            'j_idt17%3Aedit-participantTypeCheckbox': ['FIRSTINSTANCE', 'APPEAL', 'CASSATION'],
            'j_idt17%3Aedit-participant': '',
            'j_idt17%3Aedit-dateFrom': '01.01.2018',
            'j_idt17%3Aedit-dateFrom-hid': '01.01.2018',
            'j_idt17%3Aedit-dateTo': '31.12.2018',
            'j_idt17%3Aedit-dateTo-hid': '31.12.2018',
            'j_idt17%3Aedit-category': '', 
            'j_idt17%3Aedit-district': '1',
            'j_idt17%3Aedit-court': '', 
            'j_idt17%3AiinOrBin':'', 
            'j_idt17%3Aplaintff':'', 
            'j_idt17%3Adefendant':'', 
            'j_idt17%3Aattorney':'', 
            'j_idt17%3Aedit-consideration':'',
            'javax.faces.ViewState': '-2933287602839480198:8530075810638410425',
            'javax.faces.source': 'j_idt17:edit-participantTypeCheckbox:2',
            'javax.faces.partial.event': 'change',
            'javax.faces.partial.execute': 'j_idt17%3Aedit-participantTypeCheckbox j_idt17%3Aedit-participantTypeCheckbox:1',
            'javax.faces.partial.render': 'casePanel',
            'javax.faces.behavior.event': 'change',
            'AJAX%3AEVENTS_COUNT': '1',
            'rfExt': 'null',
            'javax.faces.partial.ajax': 'true' 
        }
        '''
        data = {
            
            'edit-period: ': '2018',
            'edit-dateFrom': '01.01.2018'
        }        
        '''
        
        r = s.post('http://office.sud.kz/courtActs/site/index.xhtml', data=data, cookies=my_cookies,headers=headers)

        print r.status_code

        print r.text

        r = s.get('http://office.sud.kz/courtActs/site/lawsuitList.xhtml', cookies=my_cookies)
        #print r.cookies.get_dict()
        f = open('test.html', 'w')
        f.write(r.text.encode('utf-8'))
        f.close()
        