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
from main.tools import getSessionId, readSessionId, getSessionId

def chekForm(html):
    soup = BeautifulSoup(html, 'html.parser')
    inputs = soup.findAll("input")  
    if len(inputs)>1:
        return False
    else:
        return True

class Command(BaseCommand):

    def handle(self, *args, **options):
        print 'Start importing'
        s = requests.Session()
        print readSessionId()
        cookies = {"SessionId": readSessionId()}
        url = 'http://online.zakon.kz/sud/search?sides_phrase=1&context_phrase=1&files=1&sort=date_desc'
        r = s.get(url,headers=headers,cookies=cookies)
        print r.text
        if chekForm(r.text):
            print r.text
        else:
            getSessionId()


        
