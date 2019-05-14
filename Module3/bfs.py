#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 14 11:17:39 2019

@author: anees
"""

from bs4 import BeautifulSoup
#import urlparse
import urllib
from urllib.parse import urljoin
from contextlib import suppress
from urllib.request import urlopen, Request
import bs4

url = "https://associationofengineers.com/"

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}




#historic record of the websites already visited
visited = [url]

req=Request(url,headers=headers)        # html download using urllib
page=urlopen(req).read()            
soup=bs4.BeautifulSoup(page,features="lxml")
allItems = soup.findAll("a", href = True)            #formatting html using beautiful soup
    

#print allItems
junk = []
for item in allItems:
    
    item["href"] = urljoin(url, item["href"])
    if url in item["href"] and item["href"] not in visited:
        visited.append(item["href"])
        print(str(item["href"]))
# =============================================================================
#         req=Request(str(item["href"]),headers=headers)        # html download using urllib
#         page=urlopen(req).read()            
#         soup=bs4.BeautifulSoup(page,features="lxml")
#         print(soup.prettify()) 
# =============================================================================
    if url not in item["href"]:
        junk.append(item["href"])

#print(visited)