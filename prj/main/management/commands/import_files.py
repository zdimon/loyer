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
from main.models import Files


   

class Command(BaseCommand):

    
   
    def handle(self, *args, **options):
        directory = '/home/zdimon/storage2/home/zarik/www/loyer/TXT2018'
        print "Start"
        #print "Delete records"
        #Files.objects.all().delete()
        cnt = 0
        for filename in os.listdir(directory):
            if filename.endswith(".txt"): 
                fname = os.path.join(directory, filename)
                f = open(fname,'r')
                content = f.read()
                f.close()
                f = Files()
                f.txt = content
                f.url = filename
                f.save()
                cnt += 1
                print "Saving .... %s " % cnt
                
