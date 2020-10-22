#!/usr/bin/env python
# coding: utf-8

# ## Preliminaries

# In[1]:


#!usr/bin/python
import pandas as pd
# import numpy as np
from bs4 import BeautifulSoup
# from ast import literal_eval
import requests, datetime, time
import json


# In[2]:


# Bring in auctions html

headers = {
    'User-Agent': 'AV User Agent 20201011',
    'From': 'anvance@gmail.com'
}


# In[3]:


site = requests.get('https://bringatrailer.com/auctions', headers=headers)
site.status_code


# ## Parse active auctions

# In[4]:


# Soup it
soup = BeautifulSoup(site.text, 'html.parser')


# In[5]:


# parse and build tuples for a table

labels = ['uid',
          'listing_title', 
          'listing_excerpt', 
          'listing_link', 
          'latest_bid', 
          'year',
          'make',
          'model',
          'category',
          'keyword',
          'vin',
          'latitude',
          'longitude']

listing_tuples = []


# In[6]:


for item in soup.findAll('div', class_ = lambda x: (x == 'auctions-item-container'))[1:]:
    try:
        uid = item['data-update']    
    except AttributeError:
        uid = 'not found'
    try:
        listing_title = item.find('h3',class_='auctions-item-title').text    
    except AttributeError:
        listing_title = 'not found'
    try:
        listing_excerpt = item.find('div', class_='auctions-item-excerpt').text
    except AttributeError:
        listing_excerpt = 'not found'
    try:
        listing_link = item.find('h3').find('a', attrs = {'href': True})['href']
    except AttributeError:
        listing_link = 'not found'
    try:
        latest_bid = item.find_all('span', attrs= {'data-current': True})[0]['data-current']
    except AttributeError:
        latest_bid = 'not found'
    try:
        year = json.loads(item['data-searchable'])['year']
    except AttributeError:
        year = 'not found'
    try:
        make = json.loads(item['data-searchable'])['make']
    except AttributeError:
        make = 'not found'
    try:
        model = json.loads(item['data-searchable'])['model']
    except AttributeError:
        model = 'not found'
    try:
        category = json.loads(item['data-searchable'])['category']
    except AttributeError:
        category = 'not found'
    try:
        keyword = json.loads(item['data-searchable'])['keyword']
    except AttributeError:
        keyword = 'not found'
    try:
        vin = json.loads(item['data-searchable'])['vin']
    except AttributeError:
        vin = 'not found'
    try:
        latitude = item['data-lat']
    except AttributeError:
        latitude = 'not found'
    try:
        longitude = item['data-lon']
    except AttributeError:
        longitude = 'not found'
    listing_tuple = (uid,
                     listing_title, 
                     listing_excerpt, 
                     listing_link, 
                     latest_bid, 
                     year,
                     make,
                     model,
                     category,
                     keyword,
                     vin,
                     latitude,
                     longitude)
    listing_tuples.append(listing_tuple)


# In[7]:


staging_df = pd.DataFrame(listing_tuples, columns = labels)


# In[8]:


time_string = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d_%H-%M-%S')
time_string_2 = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')


# In[9]:


staging_df['scrape_ts'] = time_string_2


# In[10]:


staging_df.to_csv('../../bat-2020-data/bat_listings_output_%s.csv' % time_string, index=True)


# ## Parse auction results

# In[11]:


results = requests.get('https://bringatrailer.com/auctions/results', headers=headers)


# In[12]:


results.status_code


# In[13]:


results_soup = BeautifulSoup(results.text)


# In[14]:


columns = ['title','result', 'link']
results_list = []
for item in results_soup.find_all('div', class_='exceptional-item-extended'):
    title = item.find('a').text
    result = item.find('div', class_='exceptional-item-status').text
    link = item.find('a')['href']
    results_tuple = (title, result, link)
    results_list.append(results_tuple)
for item in results_soup.find_all('div', class_='auctions-item-extended'):
    title = item.find('span').text
    result = item.find('div', class_='auctions-item-status').text
    link = item.find('a')['href']
    results_tuple = (title, result, link)
    results_list.append(results_tuple)


# In[15]:


results_df = pd.DataFrame(results_list, columns=columns)


# In[16]:


time_string = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d_%H-%M-%S')
results_df.to_csv('../data/bat_results_output_%s.csv' % time_string, index=True)


# In[ ]:




