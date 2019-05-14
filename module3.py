#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  5 21:40:11 2019

@author: anees
"""
import happybase
import time
import datetime
import bs4
from urllib.request import urlopen, Request
from urllib.parse import urljoin
from contextlib import suppress
import re
import os
from hdfs import InsecureClient


present_dir=os.getcwd()
location=present_dir+'/Module3/html'



host='127.0.0.1'
port=9090
table_read='eng_test'
#table_write='faculty_usa2'
url_no=3

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
client_hdfs = InsecureClient('http://localhost:50070')

#################################function definition below#################################

def html_parse(link):
    req=Request(link,headers=headers)        
    page=urlopen(req).read()            
    soup=bs4.BeautifulSoup(page,features="lxml")            
    html_text=soup.prettify()
    return html_text,soup
    

def local_file_write(searchterm,urlno,html):
    f = open(location+'/'+searchterm+str(urlno)+'.html', 'w')   #new html file creation
    f.write(html)
    f.close()
    

def hdfs_file_write(searchterm,urlno,html) :
    with client_hdfs.write('/user/colleges/'+searchterm+str(urlno)+'.html', encoding = 'utf-8') as writer:
                writer.write(html)


def embeddurl_table(searchterm,urlno,souper):
    i=1
    for link in souper.findAll('a', attrs={'href': re.compile("^http://")}):
        if(i<5):
            [htmltext1,s]=html_parse(str(link.get('href')))
            print(str(urlno)+'_'+str(i))
            local_file_write(searchterm,str(urlno)+'_'+str(i)+'atag',htmltext1)
        else:
            break
        i+=1
        

def bfs_html(searchterm1,urlno1,url,souper1):  
    allItems = souper1.findAll("a", href = True)
    visited=[]
    
    i=0
    for item in allItems:
        i+=1
        item["href"] = urljoin(url, item["href"])
        if url in item["href"] and item["href"] not in visited:
            visited.append(item["href"])
            [htmltext1,s]=html_parse(str(item["href"]))
            print(str(urlno1)+'_'+str(i))
            local_file_write(searchterm1,str(urlno1)+'_'+str(i),htmltext1)
            
            
##################################main code################################################        
time_start=time.time()
date_time_start=str(datetime.datetime.now())
file_counter=0
input_url_count=0


c = happybase.Connection(host,port)
table=c.table(table_read)

#tabe listing and creating new hbase table 
# =============================================================================
# all_tables=c.tables()
# table_list=[x.decode('utf-8') for x in all_tables]
# if table_write not in table_list:
#     c.create_table(table_write,{'embedd_url': dict()}) 
# table_2=c.table(table_write)
# 
# =============================================================================

#scanning over hbase table
for key, data in table.scan():
    
    keyword=str(key).split('\'')[1]             #converting row key from bytes to string
    row = table.row(key, columns=[b'url'])      #selecting rows from table with column family url
    
    for k in range(1,url_no+1):
        input_url_count+=1
        with suppress(Exception):
        
            combstr='url:'+str(k)
            byt_str=bytes(combstr,'utf-8')
            url=str(row[byt_str]).split('\'')[1]      #converting url column family columns from bytes to string
            print(keyword+":"+str(k)+"\t"+url)
        
            [htmltext,soup]=html_parse(url)
            local_file_write(keyword,k,htmltext)
            #hdfs_file_write(keyword,k,htmltext)
            #embeddurl_table(keyword,k,soup)
            bfs_html(keyword,k,url,soup)
            file_counter+=1
            



end_time=time.time()-time_start

#print file input status
print('\n'+'date_time_start'+'\t\t\t'+'time lapsed'+'\t\t'+'No of url read'+'\t\t'+'No of files written')
print('\n'+date_time_start+'\t'+str(end_time)+'\t'+str(file_counter)+'\t\t\t'+str(input_url_count))

#write file input log into a file
with open(present_dir+'/Module3/log_module3.txt','a') as outFile:
    outFile.write('\n'+date_time_start+'\t'+str(end_time)+'\t'+str(file_counter)+'\t'+str(input_url_count)) 
            
            
        
        
    


