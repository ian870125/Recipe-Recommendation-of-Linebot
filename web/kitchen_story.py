# %%
import pandas as pd
import numpy as np
import os 
import pickle  
import time

# save env

from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.common.exceptions import NoSuchElementException #點完所有按鈕時
from selenium.webdriver.common.action_chains import ActionChains #move_to_element
from selenium.common.exceptions import StaleElementReferenceException #error > element is not attached to the page document
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from pprint import pprint
import requests
import unicodecsv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
import tqdm

import pyautogui
from  itertools import permutations
import nltk
import re


import argparse
import pprint
import gensim
#from glove import Glove
#from glove import Corpus

###  繁體中文轉換為簡體
# https://github.com/BYVoid/OpenCC
import opencc


import urllib.request
from PIL import Image
#import m3u8_To_MP4

# %%
################################################################################
###################  kitchen story webcrawler function  ########################
################################################################################
def replace_string(x):
    try:
        for r in (("k" ,"000"), (",", ""),('.','')):
            x = x.replace(*r)
    except:
        pass
    return x 



def  kitchen_story_basic_info(number,*args):
    ## open web
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  
    driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=options)
    driver.maximize_window()
    driver.get("https://www.chufanggushi.com/sou-xun")
    
    ## input is a word (traditional to simple)
    converter_Simple = opencc.OpenCC('tw2sp.json')
    ## simple to tranditional 
    converter_TW = opencc.OpenCC('s2twp.json')
    
    
    ## convert tranditional word to simple
    simpleWord =  [''.join(converter_Simple.convert(tranditional_word)) for tranditional_word in args[0]]
    search_word = ' '.join(map(str, simpleWord))
    
    ## search recipe 
    search_box = '#js-app > div.ui-header > div.ui-header__header > div.ui-header-combobox.ui-header__combobox > div > input'
    WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, search_box))).send_keys(search_word, Keys.ENTER)

    ## create df
    df = pd.DataFrame(columns=['Like_num','Time','Name','URL','img'])

    ## get list of recipe
    for i in range(1,number):
        
        try:
            ## get basic information
            basic_info = driver.find_element(By.CSS_SELECTOR,f'#search-app > section > ul > li:nth-child({i})')
            temp = [converter_TW.convert(i) for i in  basic_info.text.split('\n')[:3] ]

            ## get URL
            temp.append(basic_info.find_element(By.CSS_SELECTOR,'section.archive-tile__infos > h3 > a').get_attribute("href"))

            ## get img 
            temp.append(basic_info.find_element(By.CSS_SELECTOR,f'section.archive-tile__meta-container > figure > img').get_attribute("src"))

            
            df = df.append(pd.DataFrame([temp], columns = ['Like_num','Time','Name','URL','img']), ignore_index=True)
            df['Time'] =df['Time'].replace('分鐘','', regex=True)
            df['Like_num'] = [replace_string(x) for x in df['Like_num'].tolist()]
        except:
            break

    driver.close()
    
    return df

def get_food_info(number,*args):
    ## simple to tranditional 
    converter_TW = opencc.OpenCC('s2twp.json')
    
    
    df = kitchen_story_basic_info(number,*args)
    df['ingredients'] = 0 
    df['Nutrition'] = 0 
    df['steps'] = 0 
    df['have_video'] = 0
    
    
    ## open without coming up
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  
    driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=options)
    driver.maximize_window()
    
    
    for row in range(df.shape[0]):
        time.sleep(1)
        #wait = ui.WebDriverWait(driver,10)
        driver.get(df.URL[row])
        #wait.until(lambda driver: driver.find_element(By.CSS_SELECTOR,f'#nutrition-section'))
        
       
        ## 食材克數
        ingredients=driver.find_element(By.CSS_SELECTOR,f'#ingredients-section')
        ingredients = len([converter_TW.convert(i) for i in  ingredients.text.split('\n')[1:]])-1
        
       
        ## 營養標示
        Nutrition = driver.find_element(By.CSS_SELECTOR,f'#nutrition-section')
        Nutrition = [converter_TW.convert(i) for i in  Nutrition.text.split('\n')[1:]]

        ## 步驟
        steps = driver.find_elements(By.CLASS_NAME,'step')
        temp = ''
        temp= list(map(lambda x :'\n\n'.join([temp,x.text]) , steps))
        temp = np.sum([1 for s in temp if '烹饪步骤' in s])
        
        
        ## 有沒有影片
        img_or_video = driver.find_element(By.CLASS_NAME,'page-header')
        try :
            len(img_or_video.find_element(By.CSS_SELECTOR,'div > video').get_attribute('src'))
            df.loc[row,['ingredients','Nutrition','steps','have_video']] = [ingredients,Nutrition,temp,'Y']
        except:
            df.loc[row,['ingredients','Nutrition','steps','have_video']] = [ingredients,Nutrition,temp,'N']
            


    
    driver.close()
    return df





# %%
## test function 

if __name__=='__main__':
    testdf=get_food_info(5,'鸡肉')



