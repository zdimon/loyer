# -*- coding: utf-8 -*-
import requests
import sys
import os
from bs4 import BeautifulSoup
import os.path
import time
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36',
    'Accept': 'ext/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' ,
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language':'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache'
    
}

def getSessionId():

    s = requests.Session()
    r = s.get('https://auth.zakon.kz/account/login',headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    sign = soup.find("input", {"name": "__RequestVerificationToken"})  
    sec_cookie =  r.cookies.get_dict()
    
    # POST
    
    data = {
            "Login":"0595586181", 
            "Password":"5634290166",
            "__RequestVerificationToken": sign["value"],
            "Remember": "false",
            "ReturnApp": "//online.zakon.kz/",
            "ReturnUrl": ""
            }
    r = s.post('https://auth.zakon.kz/login',data=data, headers=headers, cookies=sec_cookie, allow_redirects=False)
    for k in r.cookies.get_dict().keys():
        sec_cookie[k] = r.cookies.get_dict()[k]    
    
    # AUTH Location
    
    headers['Host'] = 'auth.zakon.kz'
    headers['Referer'] = 'https://auth.zakon.kz/account/login'
    r = s.get('https://auth.zakon.kz/login/autologin?returnApp=%2F%2Fonline.zakon.kz%2F',headers=headers, cookies = sec_cookie, allow_redirects=False)
    print r.status_code
    location = r.headers['Location']    
    
    time.sleep(2)
    sec_cookie['computerId'] = 'e3e82ae6-3b9d-4bc3-a453-7a1ad1d81388'
    sec_cookie['currentBase'] = 'MQ=='
    headers['Host'] = 'online.zakon.kz'
    headers['Upgrade-Insecure-Requests'] = '1'
    print 'Try to go to 301 loc %s' % location
    try:
        r = s.get(location,headers=headers, cookies = sec_cookie, allow_redirects=False)
        print r.status_code
        session_id = s.cookies.get_dict()['SessionId']  
        print r.cookies.get_dict()
        print 'Session ID: %s' %  session_id 
        with open('session_id', 'w') as f:
            f.write(session_id)
    except:
        print 'Error request %s' % location
        return 1
        #with open('session_id', 'w') as f:
        #    f.write('None')

    url = 'http://online.zakon.kz/sud/'
    r = s.get(url, headers=headers, cookies = sec_cookie, allow_redirects=False)
    print r.cookies.get_dict()
    try:
        r.cookies.get_dict()['PHPSESSID']
        with open('phpsessid', 'w') as f:
            f.write(r.cookies.get_dict()['PHPSESSID'])
        sec_cookie['PHPSESSID'] = r.cookies.get_dict()['PHPSESSID']
    except:
        print 'can not find PHPSESSID!!!'
    time.sleep(2)
    location = r.headers['Location']
    print 'Try to go to 301 loc %s' % location
    try:
        r = s.get(location,headers=headers, cookies = sec_cookie, allow_redirects=False)
        print r.status_code
        session_id = s.cookies.get_dict()['SessionIdv2']  
        print r.cookies.get_dict()
        print 'Session ID v2: %s' %  session_id 
        with open('session_idv2', 'w') as f:
            f.write(session_id)
    except:
        print 'Error request %s' % location
        return 1

def readSessionId():
    fname = 'session_id'
    #if os.path.isfile(fname):
    f = open(fname,'r')
    session_id = f.read()
    f.close()
    return  session_id.replace('\n', ' ')
    #else: 
    #    return 0
     
     
def readPHPSessionId():
    fname = 'phpsessid'
    #if os.path.isfile(fname):
    f = open(fname,'r')
    session_id = f.read()
    f.close()
    return  session_id.replace('\n', ' ')
            

def checkDocument(html):
    soup = BeautifulSoup(html, 'html.parser')   
    #try:
    d = soup.find("div", {"id": "noDocAccess"})
    if d == None:
        return True
    else:
        return False


def saveArticle(id,session_id):

    #directory = "data/docs/%s" % page
    #if not os.path.exists(directory):
    #    os.makedirs(directory)
    id = str(id)
    cookies = {"SessionId": session_id}
    fn = 'data/docs/%s.html' % id
    url = 'https://online.zakon.kz/Document/Document.aspx?doc_id=%s&sublink=0&mode=all&action=print&comments=on&user_comments=on&size=1' % id
    txt = requests.get(url, cookies=cookies,headers=headers ).text
    if(checkDocument(txt)):
        f = open(fn,'w')
        f.write(txt.encode('utf-8'))
        f.close()  
        print 'Success writing %s!!!' % id
    else:
        print txt
        print 'We need to relogin'
   
   
def savePageDocuments(page):     
    fn = 'data/pages/%s' % page
    try:
        f = open(fn,'r')
        items = json.loads(f.read())
        f.close()    
    except:
        print 'There is not page %s ' % page
        return False
    for p in items:
        saveArticle(p,readSessionId())
      
        
def savePageList(page):
        
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
                data.append(tmp[1])
              
        except Exception, e :
            #print str(e)
            pass
      
    fn = 'data/pages/%s' % page
    f = open(fn,'w')
    f.write(json.dumps(data))
    f.close()        
        
        
    
# MjE4NDI5MzQ=  MTYwMDMzMDk= MzIyNDM4NDk=
    
#saveArticle('37680375','NDI4MTk5NTQ=')

#savePageDocuments(1)

#getSessionId()

#savePageList(793)


