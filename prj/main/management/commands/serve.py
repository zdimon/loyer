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


def getCountDocs(txt):
    import re
    result = re.search('Найдено дел:(.*)\(отображаются', txt)
    return int(result.group(1))



                

class Command(BaseCommand):




    def handle(self, *args, **options):
        print 'Start'
        for d in Documents.objects.filter(date='2018-09-04'):
            print 'Process %s' % d.uid
            getFiles(d)
        '''
        f = open('log.html','r')
        txt = f.read()
        f.close()
        print getCountDocs(txt)
        '''

