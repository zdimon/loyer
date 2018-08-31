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

def checkDocument(html):
    soup = BeautifulSoup(html, 'html.parser')   
    #try:
    d = soup.find("div", {"id": "noDocAccess"})
    if d == None:
        return True
    else:
        return False

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
    try:
        r = s.get(location,headers=headers, cookies = sec_cookie, allow_redirects=False)
        print r.status_code
        session_id = s.cookies.get_dict()['SessionId']  
        print 'Session ID: %s' %  session_id 
        with open('session_id', 'w') as f:
            f.write(session_id)
    except:
        print 'Error request %s' % location
        #with open('session_id', 'w') as f:
        #    f.write('None')


def saveDocument(id,session_id):
    #directory = "data/docs/%s" % page
    #if not os.path.exists(directory):
    #    os.makedirs(directory)
    id = str(id)
    cookies = {"SessionId": session_id}
    fn = 'data/docs/%s.html' % id
    url = 'https://online.zakon.kz/Document/Document.aspx?doc_id=%s&sublink=0&mode=all&action=print&comments=on&user_comments=on&size=1' % id
    txt = requests.get(url, cookies=cookies,headers=headers ).text
    if(checkDocument(txt)):
        d = Documents.objects.get(uid=id)
        d.content = txt
        d.is_downloaded = True
        d.save() 
        d.clearHtml()
        print 'Success writing %s!!!' % id
    else:
        #print txt
        print 'We need to relogin'

def readSessionId():
    fname = 'session_id'
    f = open(fname,'r')
    session_id = f.read()
    f.close()
    return  session_id

class Command(BaseCommand):

    def handle(self, *args, **options):
        print 'Start importing documents'
        session_id = readSessionId()
        for d in Documents.objects.filter(is_downloaded=False).order_by('id'):
            saveDocument(d.uid,session_id)
        #getSessionId()

