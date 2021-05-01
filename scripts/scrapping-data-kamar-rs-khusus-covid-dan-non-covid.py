#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from bs4 import BeautifulSoup as soup
import csv
from pathlib import Path

import datetime

now = datetime.datetime.now()


# In[2]:


import selenium
from selenium import webdriver


# In[3]:


# konfigurasi chromedriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--window-size=1420,1080')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

browser = webdriver.Chrome(chrome_options=chrome_options)


# In[4]:



data_folder = Path("data/")
file_data = 'data_kamar_detail' + now.strftime("%Y%m%d") + '-' + now.strftime("%H%M") + '.csv'
filename = data_folder / file_data
csvFile = open(filename, 'a')
#Use csv Writer
csvWriter = csv.writer(csvFile)
csvWriter.writerow(['satker', 'nama', 'alamat', 'prov', 'jenis_ruang', 'ruang', 'total_kamar', 'total_terisi', 'total_kosong', 'last_update','lat','lng'])


# In[5]:


faskes_df = pd.read_csv("list-faskes-filtered.csv",delimiter=',',encoding='ISO-8859-1')
#faskes_df.head()


# In[ ]:


for index, row in faskes_df.iterrows():
    
    satker = str(row['kode_rs'])
    nama_rs = str(row['nama_unit'])
    alamat =  str(row['alamat'])
    prov =  str(row['nama_prov'])
    lat =  row['lat']
    long =  row['lng']
    
    _jenis_ruang = '-'
    _ruang = '-'
    _total_kamar = '0'
    _total_kosong = '0'
    _total_isi = '0'
    _last_update = '-'
    
    i=1
    while(i<=2): 
        #if (satker == '3471052'):
        link = 'http://yankes.kemkes.go.id/app/siranap/tempat_tidur?kode_rs='+satker+'&jenis='+str(i)
        browser.get(link)
        #print(r)
        data = browser.page_source
        url = soup(data,"lxml")
        print(str(satker)+'-'+str(i))
        card = url.find_all('div', attrs={'class':'card h-100'})
        #print(nama_rs)
        if card is not None:
            for col in card:
                _satker = satker
                _nama = nama_rs
                _alamat = alamat
                _prov = prov
                _lat = lat
                _long = long
                if (i==1):
                    _jenis_ruang = 'Tempat Tidur Covid 19'
                elif (i==2):
                    _jenis_ruang = 'Tempat Tidur Non Covid 19'
                _ruang = col.find('h5', attrs={'class':'text-center'}).text
                #print(str(_ruang))
                _total_kamar = col.find('div', attrs={'class':'col-4 offset-2 pl-0 pr-0 col-md-4 offset-md-2 border text-center mr-2 pt-1'}).find('h1').text
                _total_kosong = col.find('div', attrs={'class':'col-4 pl-0 pr-0 col-md-4 border text-center pt-1'}).find('h1').text
                _total_terisi = int(_total_kamar) - int(_total_kosong)
                _last_update = col.find('div', attrs={'class':'ml-auto mt-1'}).text

                csvWriter.writerow([_satker, _nama, _alamat, _prov, _jenis_ruang, _ruang, _total_kamar, _total_terisi, _total_kosong, _last_update, _lat, _long])
        i+=1


# In[ ]:


csvFile.close()


# In[ ]:


dataset = pd.read_csv(filename)
dataset.shape


# In[ ]:


dataset.head(12)


# In[ ]:


#import pandas_profiling
#dataset.profile_report()

