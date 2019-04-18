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
    sl = random.randint(3,6)
    print 'sleeping %s' % sl
    time.sleep(sl)

def getCountDocs(txt):
    import re
    if txt.find('Найдено дел: 0')>0:
        return 0
    
    #print txt
    result = re.search('Найдено дел:(.*)\(отображаются', txt)
    cnt = result.group(1) 
    cnt = cnt.replace(' ','')
    #txt = txt.replace(' ','')
    return int(cnt)




def getFiles(d):
    soup = BeautifulSoup(d.doc_html, 'html.parser')
    divs = soup.findAll('td')
    #import pdb; pdb.set_trace()
    for div in divs:
        try:
            a = div.find('a')
            url = 'http://online.zakon.kz/sud/'+a['href']
            txt = makeRequest(url)
            f = Files()
            f.document = d
            f.html = txt
            f.save()
            f.clearHtml()
            print 'File saved!!!'
        except Exception, e:
            pass


            #print str(e)


def makeDateFormat(dt):
    tmp = dt.split('-')
    return '%s-%s-%s' % (tmp[2],tmp[1],tmp[0]) 




def makeRequest(url):
    try:
        txt = requests.get(url,headers=copy_header,cookies=copy_cookie).text     
        return txt       
    except requests.exceptions.ReadTimeout as errh:
        print ("Http Error timeout!")   
    except:
        randomDelay()
        print 'Pepeat request'
        makeRequest(url)


def clear(txt):
    return txt.replace('\n','').replace('\t','')


def getDate():
    f = open('date','r')
    date = f.read()
    f.close()
    return date

def addDay(date):               
    dt = datetime.strptime(date, '%d-%m-%Y')
    return dt + datetime.timedelta(days=1)


def parseRow(row):
    tds =  row.findAll("td")
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

        try:
            out['href'] = name['href']
        except Exception, e:
            print str(e)
        return out
    else:
        return False

def savePage(html):
    
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
            try:
                c.save()
                print 'Done!!! %s' % c.uid
            except Exception, e:
                print 'Error saving. Duplicate!'
                print str(e)
        #else:
        #    import pdb; pdb.set_trace()
    cnt = Documents.objects.all().count()
    print 'Total: %s' % cnt
    


def getListTmp(date,page=1):
    url = 'http://online.zakon.kz/sud//search?check=1&sort=date_desc&region=-&court=-&date_start=%s&date_end=%s&type=-&files=1&number=&sides=&sides_phrase=1&judge=&context=&context_phrase=1&page=%s' % (date,date,page)
    txt = makeRequest(url,cookies=copy_cookie, headers=copy_header).txt

#def test():
#    def int():

def gidrateList(dict):
    out = []
    for i in dict:
        if len(i['content']) == 0:
            url = i['url']
            i['content'] = makeRequest(url)
            print 'gidrating %s' % i['page']
            print 'url: %s' % url;
            randomDelay()
        out.append(i)
        
    return out

def getList(date):
    out = []
    '''
    f = open('test/1.html', 'r') 
    txt = f.read()
    f.close()
    '''
    params = {
    'sort': 'date_desc',
    'date_start': date,
    'date_end': date,
    'type': '-',
    'files': '1',
    'sides_phrase': '1',
    'context_phrase': '1',
    'page': '1'
    }
    url = 'http://online.zakon.kz/sud//search'
    url = 'http://online.zakon.kz/sud/search?date_start=%s&date_end=%s&sides_phrase=1&context_phrase=1&files=1&sort=date_desc' % (date,date)
    
    txt = makeRequest(url)
    #print url

    f = open('log.html', 'w') 
    f.write(txt.encode('utf-8'))
    f.close()

    cnt = getCountDocs(txt.encode('utf-8'))
    
    l = Log()
    l.date = makeDateFormat(date)
    l.cnt = cnt
    try:
        l.save()
        l.update()
    except:
        print 'Log for %s is exist' % date

    if cnt == 0:
        return False

    if cnt<=30:
        cp = 1
    elif cnt%30>0:
        cp = (cnt/30)+1
    else:
        cp = cnt/30
    
    for p in range(1,cp+1):
        url = 'http://online.zakon.kz/sud//search?&date_start=%s&date_end=%s&sides_phrase=1&context_phrase=1&files=1&page=%s&sort=date_desc' % (date,date, p)
        if p == 1:
            out.append({
                "url": url,
                "page": p,
                "content": txt
            })
        else:
            out.append({
                "url": url,
                "page": p,
                "content": ''
            }) 
           



    '''
    soup = BeautifulSoup(txt, 'html.parser')
    ul = soup.find('ul',{"class": "pagination"})
    cnt = 1
    try: 
        lis = ul.findAll('li')
    except:
        print 'No data for date %s' % date
        return False

    for li in lis:
        try:
            if cnt == 1:
                out.append({
                    "url": li.find('a')['href'],
                    "content": txt
                })
            else:
                out.append({
                    "url": li.find('a')['href'],
                    "content": ''
                })         

            cnt = cnt+1
        except:
            pass
    '''

    return out

   
def loadDocs(date):
    print 'Loading documents'
    for d in Documents.objects.filter(date=date):
        if d.is_document_downloaded == False:
            print 'case %s' % d.uid   
            url = 'http://online.zakon.kz/sud//'+d.href   
            print 'Loading %s' % url
            txt = makeRequest(url)
            d.doc_html = txt
            d.is_document_downloaded = True
            d.save()
            d.clearDocHtml()
            print 'Saving done %s!!!' % d.uid
            randomDelay()
        else:
            print 'Already downloaded!!!'
        #getFiles(d)

class Command(BaseCommand):

    
    def add_arguments(self, parser):
        parser.add_argument('-s', dest='start')
        parser.add_argument('-e', dest='end')

    def handle(self, *args, **options):
        start_date = options["start"]
        end_date = options["end"]
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        date_generated = [end_date - timedelta(days=x) for x in range(0, (end_date-start_date).days)]

        print 'Start step importing from %s to %s' % (start_date, end_date)
        #print date_generated
        #sys.exit()
        #dt = getDate()
        #dt = '29-08-2018'
        #print 'Process %s' % dt
        
        add = []
        for l in Log.objects.all():
            if l.cnt!=l.fact:
                add.append(l.date)
        #print add
        #sys.exit()
        print date_generated
        #sys.exit()
        #for date in add:
        for date in date_generated:
            try:
                l = Log.objects.get(date=date)
                if l.cnt==l.fact:
                    print 'Date %s is full of data!!!!' % l.date
                    continue
            except:
                pass
            
            ## Selete all for date
            Documents.objects.filter(date=date).delete()
            
            
            dt = date.strftime("%d-%m-%Y")
            lst = getList(dt)
            if lst:
                for p in gidrateList(lst):
                    try:
                        savePage(p['content'])
                    except:
                        pass

                l = Log.objects.get(date=date)
                l.update()
            #loadDocs(makeDateFormat(dt))
        #for url in getListMock(dt):
        #    print 'load %s' % url

       
