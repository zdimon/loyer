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

copy_cookie = {
    'ASP.NET_SessionId':'og1dxrw53utcjaqaghcg1jbl',			
    'AST':'kpVRl1RehEiNpSjYESNSAA==',				
    'ASTI':'lTPqHm2RS0q62jrkQkwQZA==',			
    'PHPSESSID':'gg7lepus665dv1kn6jsp91vsp1',				
    'SessionId':'Njc5MDE3NDE=',				
    'SessionIdv2':'eyJ0b2tlbiI6ImtwVlJsMVJlaEVpTnBTallFU05TQUE9PSIsInRva2VuSXRlbSI6ImxUUHFIbTJSUzBxNjJqcmtRa3dRWkE9PSJ9',		
    '__gads':'ID=5c52c27084d1b456:T=1535618952:S=ALNI_MbrdGKRJMfVU1igmqu_hnvczI45WA',				
    '_ga':'GA1.2.1248454394.1535618146',				
    '_gat':'1',				
    '_gid':'GA1.2.1050935430.1536073977',				
    '_ym_d':'1535618145',				
    '_ym_uid':'1535618145559761940',				
    '_zero_cc':'65b891b2777303',			
    '_zero_ss':'5b90d367d8f13.1536217959.1536217967.3',				
    'computerId':'86f59bd3-a601-420f-873b-d9a99c35f58f',				
    'currentBase':'MQ==',			
    'lt_uid':'79311587-9d9e-41db-8db9-3ead52db0109',			
    'pop_ad_edu2018_shown':	'true',
    'rel_val':	'600000',				
    'remember_akciya_prof_buh':	'true',				
    'searchback': ''	
}

copy_header = {
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
'Cache-Control':'no-cache',
'Connection':'keep-alive',
'Host':'online.zakon.kz',
'Pragma':'no-cache',
'Referer':'http://online.zakon.kz/sud//search?&sides_phrase=1&context_phrase=1&files=1&page=2&sort=date_desc',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36'
}



# dobles http://online.zakon.kz/sud//search?number=%E2%84%967525-17-00-1%2F667&sides_phrase=1&context_phrase=1&files=1&sort=date_desc

def chekForm(html):
    soup = BeautifulSoup(html, 'html.parser')
    inputs = soup.findAll("input")  
    if len(inputs)>1:
        return False
    else:
        return True
        
def clear(txt):
    return txt.replace('\n','').replace('\t','')
        
def parseRow(row):
    tds =  row.findAll("td")
    #len(tds)
    if len(tds) == 4:
        out = {}
        
        try:
            out['date'] = clear(tds[2].text)
        except:
            pass 
        try:
            name = tds[3].find('a')
            out['name'] = clear(name.text)
            out['number'] = name.find('b').text
        except Exception, e:
            print str(e)
            #import pdb; pdb.set_trace()
            
        try:
            out['href'] = name['href']
        except Exception, e:
            print str(e)
            #import pdb; pdb.set_trace()        
            
            
    #id = name.find('b').text
    #out['number'] = id.text
        return out
    else:
        return False
       
       
def makeDateFormat(dt):
    tmp = dt.split('-')
    return '%s-%s-%s' % (tmp[2],tmp[1],tmp[0])       
        
def savePage(html,page):
    
    soup = BeautifulSoup(html, 'html.parser')
    for tr in soup.findAll("tr",{"class": "row"}):
        data = parseRow(tr)
        if data:
            #print 'Saving %s' % page
            c = Documents()
            c.href = data['href']
            c.uid = data['number']
            c.title = data['name']
            c.date = makeDateFormat(data['date'])
            c.page = page
            try:
                c.save()
            except Exception, e:
                print 'Error saving. Duplicate!'
                print str(e)
    cnt = Documents.objects.all().count()
    print 'Total: %s' % cnt
    sl = random.randint(1,3)
    print 'sleeping %s' % sl
    time.sleep(sl)

            
def getLastPage():
    c = Documents.objects.all().order_by('-id')[0]
    return c.page
    
def getUrlResult(url,cookies):
    #print 'Start downloading %s' % url
    try:
        txt = requests.get(url,headers=copy_header,cookies=cookies).text     
        return txt       
    except requests.exceptions.ReadTimeout as errh:
        print ("Http Error timeout!")
        time.sleep(5)
        getUrlResult(url,cookies)
        
def processPages(page):
    cnt = 0
    print 'Process %s page' %  page
    fname = 'pages/%s.html' % page

    if os.path.isfile(fname):
        f = open(fname,'r')
        txt = f.read()
        f.close()
    else: 
        s = requests.Session()
        phpsessid = readPHPSessionId()
        cookies = {'PHPSESSID': phpsessid, 'SessionId': readSessionId() }
        cookies = copy_cookie

        url = 'http://online.zakon.kz/sud//search?&sides_phrase=1&context_phrase=1&files=1&page=%s&sort=date_desc' % page

        url = 'http://online.zakon.kz/sud//search?date_start=02-03-2017&date_end=02-03-2017&sides_phrase=1&context_phrase=1&files=1&sort=date_desc'

        print url
        txt = getUrlResult(url,cookies)
         
        if txt != None:
            fn = 'pages/%s.html' % page
            f = open(fn,'w')
            f.write(txt.encode('utf-8'))
            f.close()
            if os.path.getsize(fn) < 6000:
                #print 'need to relogin'
                cnt = cnt +1
                time.sleep(2)
                processPages(page)
                if cnt>3:
                    exit('Need to relogin!!!!!!!!!!!!!')
    savePage(txt,page)
    
def loopOverPage(current):
    for page in range(current,current+100):
            processPages(page)    
    time.sleep(10)
    current = current+100
    loopOverPage(current)
                          
class Command(BaseCommand):

    def handle(self, *args, **options):
        print 'Start importing'
        #getSessionId()
        #print getMaxPage()
        #sys.exit()
        
        
        #f = open('test.html','r')
        #txt = f.read()
        #f.close()
        #for page in range(1,5):
            #savePage(txt,page)
        
        #sys.exit()
        

        #print phpsessid
        #sys.exit()
        start = getLastPage()+1
        loopOverPage(start)
        #for page in range(start,start+100):
        #    processPages(page)
        #    time.sleep(2)
            

        #print cookies
        sys.exit()
        #print r.text
        if chekForm(r.text):
            print r.text
        else:
            getSessionId()


        
