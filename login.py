# -*- coding: utf-8 -*-
#sudo apt-get install python-dev libxml2-dev libxslt1-dev zlib1g-dev
import requests
import sys
import os


    
#https://auth.zakon.kz/licenses?token=9awwEWl8FUKAELt7GjvhhA%3D%3D

#https://auth.zakon.kz/license/st?tokenItem=9awwEWl8FUKAELt7GjvhhA%3D%3D&returnUrl=&returnApp=//online.zakon.kz/

#https://online.zakon.kz/ValidateAuth.aspx?token=rwp9aGy1nkmzQPwyLBoSSQ%3D%3D&tokenItem=9awwEWl8FUKAELt7GjvhhA%3D%3D&returnUrl=

s = requests.Session()

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36',
    'Accept': 'ext/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' ,
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language':'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    
}


#print(s.cookies.get_dict())


'''
data = {
        "Login":"0595586181", 
        "Password":"5634290166",
        "__RequestVerificationToken": 'CfDJ8HP9tAEEoPlFqPNLd4icIJIkqFivHbmg7-hIr6ssryhT2lCspwerYR1UGI6CG7xZVpWpALaCug2Xm1yJIRVqYPeadEAIk61joHSYUE4Pybma63hjMiY8Dfo7LQmq_RweLl1XnZUuMUEwk2guGBncOyU',
        "Remember": "false"
        }
        
        
        
url = "https://auth.zakon.kz/account/login"
r = s.post(url, data=data,headers=headers,allow_redirects=True)
print r.status_code
sys.exit("Error message")

if r.status_code == 302: # expected here
    jar = r.cookies
    redirect_URL2 = r.headers['Location']
    res2 = requests.get(redirect_URL2, cookies=jar)
    print res2.cookies.get_dict()
    

print r.cookies.get_dict()
'''
#r = s.get('https://auth.zakon.kz/account/login')

#print r.text

#response = s.get('https://online.zakon.kz/Controls/User.aspx?mode=getUserManager')


#print(s.cookies.get_dict())

session_id = 'NjQyNTIzMTc='

#print s.cookies

#for r in s.cookies:
#    print r
#sys.exit("Error message")
#txt = s.get('https://online.zakon.kz/?m=s').text

#http://online.zakon.kz/Document/Word.aspx?topic_id=35622623
# https://online.zakon.kz/Document/?doc_id=35622623
#https://online.zakon.kz/Document/Document.aspx?doc_id=35622623&sublink=0&mode=all&action=print&comments=on&user_comments=on&size=1

# 792 pages

import json
from bs4 import BeautifulSoup
#cookies = {"SessionId": "MjI0NjA5MTU="}
#url = 'https://online.zakon.kz/Document/Document.aspx?doc_id=39204650&sublink=0&mode=all&action=print&comments=on&user_comments=on&size=1'
#txt = s.get(url, cookies=cookies).text
#txt = s.get(url).text
#print txt




def saveArticle(id,page):

    directory = "data/docs/%s" % page
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    cookies = {"SessionId": session_id}
    fn = 'data/docs/%s/%s.html' % (page, id)
    url = 'https://online.zakon.kz/Document/Document.aspx?doc_id=%s&sublink=0&mode=all&action=print&comments=on&user_comments=on&size=1' % id
    txt = requests.get(url, cookies=cookies,headers=headers ).text
    f = open(fn,'w')
    f.write(txt.encode('utf-8'))
    f.close()    

def loadArticle(id):
    data = {'content':''}
    url = 'https://online.zakon.kz/Document/Document.aspx?doc_id=%s&sublink=0&mode=all&action=print&comments=on&user_comments=on&size=1' % id
    txt = requests.get(url).text
    soup = BeautifulSoup(txt, 'html.parser')
    mydivs = soup.findAll("span", {"class": "s1"})
    if len(mydivs)==1:
        data['title'] = mydivs[0].getText()
    else:
        print 'Error!! Can not find the title!'
    
    an = soup.find("td",{"id": "annotaion"})
    sp = an.findAll("span")
    try:
        data['annotation'] = sp[1].getText()
    except:
        pass
        
    divs = soup.find("td",{"class": "j33"})
    for s in divs.findAll("span"):
         data['content'] = data['content']+s.getText()   
        
        
        
        
    print an
    print data
    
#loadArticle(35622623)    
    

for counter in range(1,2):
    print 'Downloading %s' % counter

    data = {
    'mode': 'text',
    'com': 'undefined',
    'sort': '3',
    'page': counter,
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
                print tmp[1]
                data.append(tmp[1])
              
        except Exception, e :
            print str(e)
            
    fn = 'data/pages/%s' % counter
    f = open(fn,'w')
    f.write(json.dumps(data))
    f.close()
    
    for id in data:
        saveArticle(id,counter)
    break
    
 

#f = open('index.html','w')
#f.write(txt.encode('utf-8'))
#f.close()

#txt = requests.get('https://online.zakon.kz/Document/Document.aspx?doc_id=35622623&sublink=0&mode=all&action=print&comments=on&user_comments=on&size=1').text



#f = open('detail.html','w')
#f.write(txt.encode('utf-8'))
#f.close()


'''
import mammoth
with open("index.doc", "rb") as docx_file:
    result = mammoth.convert_to_html(docx_file)
    html = result.value
    print html
'''

#from docx2html import convert
#html = convert('index.docx')
#print html

#f = open('index.html','w')
#f.write(txt.encode('utf-8'))
#f.close()

#print dict(s.cookies)
print 'Done'


'''

mode: text
com: undefined
sort: 0
page: 2
text: решение суда
swhere: 3
spos: 1
tSynonym: 0
tShort: 1
tSuffix: 1
date: undefined
olds: undefined
rand: 0.20868381189161633
section: all
tDocsNoClass: 0
excludeArcBuh: 1
status: undefined


'''
