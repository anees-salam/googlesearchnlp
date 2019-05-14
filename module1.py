#!/usr/bin/env python3



import happybase
import time
import datetime
import csv
import shutil
import os


present_dir=os.getcwd()
inp=present_dir+"/Module1/Input"
processing=present_dir+"/Module1/Processing"
processed=present_dir+"/Module1/Processed"


host='127.0.0.1'
port=9090
time_start=time.time()
date_time_start=str(datetime.datetime.now())
file_counter=0
table_name='eng_test'

#table creation
c = happybase.Connection(host,port)

#check if table is present in hbase
all_tables=c.tables()
table_list=[x.decode('utf-8') for x in all_tables]

if table_name not in table_list:
    c.create_table(table_name,{'status': dict(),'url': dict()}) 
table=c.table(table_name)


for file in os.listdir(inp):
    
    #move file from input into processing
    src_file = os.path.join(inp, file)
    dst_file = os.path.join(processing, file)
    shutil.move(src_file, dst_file)
    #print(file)
    
    #file read using readcsv and inserting into hbase
    file_counter+=1
    with open(processing+"/"+file) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            hbaserow=table.row(row[0])
            if(len(hbaserow)==0):
                table.put(row[0], {"status:filename":str(file)})
    
    
    #move file from processing into processed
    src_file1 = os.path.join(processing, file)
    dst_file1 = os.path.join(processed, file)
    shutil.move(src_file1, dst_file1)
    
    
end_time=time.time()-time_start

#print file input status
print('\n'+'date_time_start'+'\t\t\t'+'time lapsed'+'\t\t'+'No of files')
print('\n'+date_time_start+'\t'+str(end_time)+'\t'+str(file_counter))

#write file input log into a file
with open(present_dir+'/Module1/log_module1.txt','a') as outFile:
    outFile.write('\n'+date_time_start+'\t'+str(end_time)+'\t'+str(file_counter))    

