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
        all_text=tuple(filter(lambda x:len(x)!=0,all_text))
    
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

    all_text=tuple(filter(lambda x:len(x)!=0,all_text))