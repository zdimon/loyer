# -*- coding: utf-8 -*-
#sudo apt-get install python-dev libxml2-dev libxslt1-dev zlib1g-dev
import requests
import sys
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
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
    'Pragma': 'no-cache'
    
}

s.get('https://online.zakon.kz/Controls/Info.aspx?mode=Logout')

r = s.get('https://auth.zakon.kz/account/login',headers=headers)

soup = BeautifulSoup(r.text, 'html.parser')
sign = soup.find("input", {"name": "__RequestVerificationToken"})
  
sec_cookie =  r.cookies.get_dict()
    
#cookie_keys = r.cookies.get_dict().keys()
#for k in cookie_keys:
#    if k.fin

#print(cookie_keys)
#sys.exit()

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

#print sec_cookie



#https://auth.zakon.kz/login/autologin?returnApp=%2F%2Fonline.zakon.kz%2F
#https://online.zakon.kz/Controls/Info.aspx?mode=Logout
headers['Host'] = 'auth.zakon.kz'
headers['Referer'] = 'https://auth.zakon.kz/account/login'
r = s.get('https://auth.zakon.kz/login/autologin?returnApp=%2F%2Fonline.zakon.kz%2F',headers=headers, cookies = sec_cookie, allow_redirects=False)
print r.status_code
location = r.headers['Location']
print location

time.sleep(2)

sec_cookie['computerId'] = 'e3e82ae6-3b9d-4bc3-a453-7a1ad1d81388'
sec_cookie['currentBase'] = 'MQ=='


headers['Host'] = 'online.zakon.kz'
headers['Upgrade-Insecure-Requests'] = '1'



print sec_cookie
print headers

#https://online.zakon.kz/ValidateAuth.aspx?token=hkQ437RoT0O0tkcH3OkJlA%3D%3D&tokenItem=VVWo4iEOtUqmzXqAevUG6g%3D%3D&returnUrl=


#location = 'https://online.zakon.kz/ValidateAuth.aspx?token=hkQ437RoT0O0tkcH3OkJlA%3D%3D&tokenItem=VVWo4iEOtUqmzXqAevUG6g%3D%3D&returnUrl='




#driver = webdriver.Chrome()
#driver.get(location)

#time.sleep(2)


#r = s.get(location,headers=headers, cookies = sec_cookie, allow_redirects=False)
#print r.status_code
#print s.cookies.get_dict()
#print r.headers


sys.exit()

cookies = {
    '.AspNetCore.Antiforgery.sYTHFp74zX4': r.cookies.get_dict()['.AspNetCore.Antiforgery.sYTHFp74zX4']
}

#print cookies

data = {
        "Login":"0595586181", 
        "Password":"5634290166",
        "__RequestVerificationToken": sign["value"],
        "Remember": "false",
        "ReturnApp": "//online.zakon.kz/",
        "ReturnUrl": ""
        }
        
print data        
        
url = "https://auth.zakon.kz/login"
r = s.post(url, data=data,headers=headers, cookies=cookies, allow_redirects=False, verify=True)

#print r.cookies.get_dict()

prgsession = r.cookies.get_dict()['PRGSession']

url = 'https://online.zakon.kz/ValidateAuth.aspx?token='+prgsession+'&tokenItem=WHHvrKzuI0GDGvPPZwFY1g%3D%3D&returnUrl='

r = s.get(url,headers=headers)

print r.cookies.get_dict()

#print prgsession

print r.status_code
