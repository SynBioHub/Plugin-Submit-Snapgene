# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 11:08:31 2020

@author: JVM
"""

import requests, ast
import datetime as dt
from html.parser import HTMLParser


html = "http://song.ece.utah.edu/examples/pages/status.php"

r = requests.get(html)

class HTMLFilter(HTMLParser):
    text = ""
    def handle_data(self, data):
        self.text += data

f = HTMLFilter()
f.feed(r.text)
res_start = f.text.find("Server status response")
res = f.text[res_start+22:]
res = ast.literal_eval(res)
expirary_date = res['licenseExpiration']
expirary_date = dt.datetime.strptime(expirary_date, '%Y-%m-%d')
today = dt.datetime.today()

if today>= expirary_date:
    print('expired')


