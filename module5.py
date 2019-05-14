#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  9 11:39:15 2019

@author: anees
"""

from nltk import sent_tokenize
from nltk import word_tokenize
from nltk.tag import StanfordNERTagger
from itertools import groupby
import re
import os
import pandas as pd


present_dir=os.getcwd()



sn_7class = StanfordNERTagger(present_dir+'/Module5/stanford_ner/classifiers/english.muc.7class.distsim.crf.ser.gz',
                               path_to_jar=present_dir+'/Module5/stanford_ner/stanford-ner.jar')


inp_location=present_dir+"/Module4/scraped_text_files"
outp_location=present_dir+"/Module5/list_of_names"


def get_individuals(ne_annot_sent):
    individuals = []
    for annot_sent in ne_annot_sent:
        #print(annot_sent)
        for tag, chunk in groupby(annot_sent, lambda x:x[1]):
            if (tag == "PERSON"):
                individuals.append(" ".join(w for w, t in chunk))
    return individuals

def extract_phone_numbers(string):
    r = re.compile(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')
    phone_numbers = r.findall(string)
    return [re.sub(r'\D', '', number) for number in phone_numbers]

def extract_email_addresses(string):
    r = re.compile(r'[\w\.-]+@[\w\.-]+')
    return r.findall(string)






for file in os.listdir(inp_location):
        f = open(outp_location+'/'+str(file).split('.')[0]+'.txt', 'w') 
        readf = open(inp_location+'/'+file, "r")
        files=readf.read()

        sentences = sent_tokenize(files)
        tokenized_sentences = [word_tokenize(sentence) for sentence in sentences]
                    
        
                    
        ne_annot_sent_7c = [sn_7class.tag(sent) for sent in tokenized_sentences]
        
        persons_sn_7class = []
        location_sn_7class= []
        organization_sn_7class=[]
        for annot_sent in ne_annot_sent_7c:
            for annot_token in annot_sent:
                if annot_token[1] == 'PERSON':
                    persons_sn_7class.append(annot_token[0])
                elif annot_token[1] == 'LOCATION':
                    location_sn_7class.append(annot_token[0])
                if annot_token[1] == 'ORGANIZATION':
                    organization_sn_7class.append(annot_token[0])
        
        f.write('\n\nLIST OF PERSONS______\n\n')
        s1='\n'.join(persons_sn_7class)
        f.write(s1)
        
        f.write('\n\nFULL NAME______\n\n')
        s1='\n'.join(get_individuals(ne_annot_sent_7c))
        f.write(s1)
        
        f.write('\n\nLIST OF LOCATION______\n\n')
        s1='\n'.join(location_sn_7class)
        f.write(s1)
        
        f.write('\n\nLIST OF ORGANIZATION______\n\n')
        s1='\n'.join(organization_sn_7class)
        f.write(s1)
        
        f.write('\n\nLIST OF email______\n\n')
        s1='\n'.join(extract_email_addresses(files))
        f.write(s1)
        
        f.write('\n\nLIST OF phone number______\n\n')
        s1='\n'.join(extract_phone_numbers(files))
        f.write(s1)
        
        name=get_individuals(ne_annot_sent_7c)
        df=pd.DataFrame({})
        
        
        
        f.close()
        readf.close()