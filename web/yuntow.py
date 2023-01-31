# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 23:16:17 2022

@author: sally
"""
import pandas as pd
import selenium
from bs4 import BeautifulSoup as bs4
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import os
#import wget
import requests 
from urllib.request import urlopen
import urllib
import random
import numpy as np


def crawer(keyword,number):

    driver = webdriver.Chrome(ChromeDriverManager().install())  #使用webdriver開啟chrome
    #driver = webdriver.Chrome() 
    url = 'https://www.ytower.com.tw/'  #網址
    driver.get(url) 

    search = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="keyword"]'))
    )
    search.send_keys(keyword)
    time.sleep(1)
    search.send_keys(Keys.RETURN)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  #將滾輪滑到底
    
    time.sleep(5)
    food_url_search = driver.find_elements(By.CSS_SELECTOR,"#recipe_suggest > ul > li > a:nth-child(1)")#抓取超連結
    food_search = driver.find_elements(By.CSS_SELECTOR, "#recipe_suggest > ul > li > a:nth-child(1) > picture > img")#抓取圖片
    food_index=[x for x in range(len(food_url_search))]
    food_name=[]
    food_image=[]
    food_url=[]
    for search in food_search:
        food_image.append(search.get_attribute("src"))
        food_name.append(search.get_attribute("alt"))
    for url in food_url_search:
        food_url.append(url.get_attribute("href"))
    allsearch=pd.DataFrame({'myindex':food_index ,'name':food_name, 'image':food_image,'url':food_url})
    number=min(number,len(allsearch))
    
    data = {}
    if number < 1:
        print("請搜尋其他關鍵字")
    else:
        for i in range(0,number):
            driver.get(allsearch.url[i])
            time.sleep(10)
            ingredients=driver.find_elements(By.CSS_SELECTOR,"#recipe_item > ul > li> span > a") 
            amounts=driver.find_elements(By.CSS_SELECTOR,"#recipe_item > ul > li> span > span") 
            ingredient_prepared=[]
            ingredient_amount=[]
            for ingredient in ingredients:
                ingredient_prepared.append(ingredient.text)
            for amount in amounts:
                ingredient_amount.append(amount.text)
            #ingredients_data=pd.DataFrame({'ingredient':ingredient_prepared ,'amount':ingredient_amount})
            methods=driver.find_elements(By.CLASS_NAME,"step") 
            method_data=[]
            for method in methods:
                method_data.append(method.text)
            tem_dict={
                'food_name':allsearch.name[i],
                'food_image':allsearch.image[i],
                'food_kinds' :len(ingredient_prepared),
                'food_steps':len(method_data),
                'url':allsearch.url[i]
            }
            data[str(i)]=tem_dict
    ingredients_min = min(data,key = lambda x:data[str(x)]['food_kinds'])#如果有兩個一樣的狀況 
    driver.get(data[ingredients_min]['url'])
    time.sleep(5)
    driver.quit()
    return(pd.DataFrame(data))
