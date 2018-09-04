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
                print 'Error saving'
                print str(e)

            
def getLastPage():
    c = Documents.objects.all().order_by('-id')[0]
    return c.page
    
def getUrlResult(url,cookies):
    print 'Start downloading %s' % url
    try:
        txt = requests.get(url,headers=headers,cookies=cookies,timeout=5).text            
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
        url = 'http://online.zakon.kz/sud/search?sides_phrase=1&context_phrase=1&files=1&sort=date_desc&page=%s' % page
        
        getUrlResult(url,cookies)
         
        
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
        for page in range(start,start+100):
            processPages(page)
            

        #print cookies
        sys.exit()
        #print r.text
        if chekForm(r.text):
            print r.text
        else:
            getSessionId()


        
