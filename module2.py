#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  3 14:36:04 2019

@author: anees
"""
import happybase
from googlesearch import search 
import time


host='127.0.0.1'
port=9090
time_start=time.time()
table_name='eng_test'
url_no=1

c = happybase.Connection(host,port)

table=c.table(table_name)


#scannig over hbase table
for key, data in table.scan():
    keyword=str(key).split('\'')[1]        #converting bytes object into string
    print(keyword)
    i=1
    for j in search(keyword,tld="co.in",num=1, stop=url_no,pause=1):    #google search keyword
        print(j)
        column="url:"+str(i)         #creating new column in column family url
        i=i+1
        table.put(keyword,{column:j})  #adding url into hbase table
        

end_time=time.time()-time_start
    




    

 
