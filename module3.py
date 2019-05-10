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
from contextlib import suppress
import re
import os
from hdfs import InsecureClient


present_dir=os.getcwd()
location=present_dir+'/Module3/html'



host='127.0.0.1'
port=9090
table_read='faculty_usa'
table_write='faculty_usa2'
url_no=3

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
client_hdfs = InsecureClient('http://localhost:50070')




def local_file_write(searchterm,urlno,html):
    f = open(location+'/'+searchterm+str(urlno)+'.html', 'w')   #new html file creation
    f.write(html)
    f.close()
    

def hdfs_file_write(searchterm,urlno,html) :
    with client_hdfs.write('/user/colleges/'+searchterm+str(urlno)+'.html', encoding = 'utf-8') as writer:
                writer.write(html)


def hbase_embeddurl_table(searchterm,url1,hb_table):
    i=1
    for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
        column="embedd_url:"+str(i)
        row_key_name=searchterm+'_'+url1
        hb_table.put(row_key_name, {column:str(link.get('href'))})
        i+=1
        

            


time_start=time.time()
date_time_start=str(datetime.datetime.now())
file_counter=0
input_url_count=0


c = happybase.Connection(host,port)
table=c.table(table_read)

#tabe listing and creating new hbase table 
all_tables=c.tables()
table_list=[x.decode('utf-8') for x in all_tables]
if table_write not in table_list:
    c.create_table(table_write,{'embedd_url': dict()}) 
table_2=c.table(table_write)


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
        
            req=Request(url,headers=headers)        # html download using urllib
            page=urlopen(req).read()            
            soup=bs4.BeautifulSoup(page,features="lxml")            #formatting html using beautiful soup
            htmltext=soup.prettify()
            
            local_file_write(keyword,k,htmltext)
            #hdfs_file_write(keyword,k,htmltext)
            #hbase_embeddurl_table(keyword,url,table_2)
            file_counter+=1
            



end_time=time.time()-time_start

#print file input status
print('\n'+'date_time_start'+'\t\t\t'+'time lapsed'+'\t\t'+'No of url read'+'\t\t'+'No of files written')
print('\n'+date_time_start+'\t'+str(end_time)+'\t'+str(file_counter)+'\t\t\t'+str(input_url_count))

#write file input log into a file
with open(present_dir+'/Module3/log_module3.txt','a') as outFile:
    outFile.write('\n'+date_time_start+'\t'+str(end_time)+'\t'+str(file_counter)+'\t'+str(input_url_count)) 
            
            
        
        
    


