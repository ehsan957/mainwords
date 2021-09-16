#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 21:46:17 2021

@author: anvaari
"""

import requests

from bs4 import BeautifulSoup

import os

import progressbar
import pickle


from hazm import  word_tokenize


def get_text_from_xml(xml_content):
    bs=BeautifulSoup(xml_content,'lxml')
    
    items=bs.find_all('item')
    
    text_list=[]
    for item in items:
        text_bs=BeautifulSoup(item.find('description').get_text(),'html.parser')
        if text_bs:
            text=text_bs.get_text()
            text_list.append(text)

    return text_list


# Specify path where this code exist
script_path=os.path.dirname(os.path.abspath(__file__))


# Iterate on urls

with open(os.path.join(script_path,'topblogsrss.txt')) as fp:
    urls=fp.readlines()
    urls=list(map(lambda x:x.strip(),urls))


if os.path.isfile(os.path.join(script_path,'all_text.txt')):
    with open(os.path.join(script_path,'all_text.txt')) as fp:
        all_text=fp.readlines()
        all_text=tuple(filter(lambda x:len(x)!=0,all_text)) # Remove empty strings
    
else:
    
    all_text=[]    
    for url,i in zip(urls,progressbar.progressbar(range(len(urls)))):
        try:
            req=requests.get(url)
        except Exception as e:
            print(f'\nException happend :\n{e}\n')
            continue
        text_list=get_text_from_xml(req.content)
        all_text+=text_list
        
    
    with open(os.path.join(script_path,'all_text.txt'),'w') as fp:
        for text in all_text:
            fp.write(text)
    # Remove empty strings
    all_text=tuple(filter(lambda x:len(x)!=0,all_text))
    
# Create a dictionary of words

words=dict()

# Specify Signs and Numbers in order to avoid words contain them enter in our final Set 
signs=['،','«','»','.',')','(','"',':',';','%','-','?',',','؛',"'",'_']
numbers=[f'{i}' for i in range(10)]
 

for text,i in zip(all_text,progressbar.progressbar(range(len(all_text)))):
    text=text.replace(u'\u200c',' ') # Remove "nim fasele"
    text_words= word_tokenize(text)
    # Remove signs and string which contains numbers
    text_words=tuple(filter(lambda x:x not in signs and all(tuple(map(lambda y:y not in numbers and y not in signs,x))),text_words))
    
    for word in text_words :
        words[word]=words.get(word,0)+1
    
words=dict(sorted(words.items(),key=lambda x:x[1],reverse=True))

with open(os.path.join(script_path,"Top100FarsiWords_py.txt"),'w') as fp:
    i=0
    for word in words:
        fp.write(word+'\n')
        i+=1
        if i==100:
            break