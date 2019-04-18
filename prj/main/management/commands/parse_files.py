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
import re


   

class Command(BaseCommand):

    
   
    def handle(self, *args, **options):
        print "Start"
        for d in Files.objects.all():
            print "Parsing .... %s" % d.url
            print d.txt
            rez = re.findall(r'[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]-[0-9]+/',d.txt)
            print rez
            break
        