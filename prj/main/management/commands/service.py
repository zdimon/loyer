# -*- coding: utf-8 -*-
#http://office.sud.kz/courtActs/site/lawsuitList.xhtml
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


class Command(BaseCommand):

    def handle(self, *args, **options):
        print 'Start looping'
       
        for d in Documents.objects.filter(is_downloaded=True).order_by('id'):
            d.clearHtml()
        #getSessionId()

