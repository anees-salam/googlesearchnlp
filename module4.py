#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  8 11:23:02 2019

@author: anees
"""
from pyspark import SparkContext
import bs4
import os


sc=SparkContext()

present_dir=os.getcwd()

inp_location=present_dir+'/Module3/html'

spark_location=present_dir+"/Module4/sparkfolder"
outp_location=present_dir+"/Module4/scraped_text_files"




for file in os.listdir(inp_location):
    f = open(outp_location+'/'+str(file).split('.')[0]+'.txt', 'w') 
    html = open(inp_location+'/'+file, "r")
    soup = bs4.BeautifulSoup(html)
    array=[]
    #rdd1=sc.parallelize(array)
    for child in soup.recursiveChildGenerator():
        name = getattr(child, "name", None)
        if name is not None:
            print('')
        elif not child.isspace(): # leaf node, don't print spaces
            line=child.strip()
            if (len(line)>10) and (len(line)<100) :
                array.append(line)
                f.write(line)
                f.write('\n')
                
    outfile=sc.parallelize(array)
    outfile.saveAsTextFile(spark_location+'/'+str(file).split('.')[0])
    f.close()

sc.stop()
    
            
             


        