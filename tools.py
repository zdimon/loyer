# -*- coding: utf-8 -*-
import requests
import sys
import os
from bs4 import BeautifulSoup


headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36',
    'Accept': 'ext/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' ,
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language':'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache'
    
}

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
    
    cookies = {"SessionId": session_id}
    fn = 'data/docs/%s.html' % id
    url = 'https://online.zakon.kz/Document/Document.aspx?doc_id=%s&sublink=0&mode=all&action=print&comments=on&user_comments=on&size=1' % id
    txt = requests.get(url, cookies=cookies,headers=headers ).text
    if(checkDocument(txt)):
        f = open(fn,'w')
        f.write(txt.encode('utf-8'))
        f.close()  
        print 'Success!!!'
    else:
        print txt
        print 'We need to relogin'
        
    
    
    
saveArticle('37680375','ODA2MDg0MTI=')
