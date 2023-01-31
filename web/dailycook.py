# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
import unittest, time, re
from webdriver_manager.chrome import ChromeDriverManager

import random
import pandas as pd

#%%
def DailyCook(material, recipe_len): #食材、想抓多少個

    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get("https://www.daydaycook.com/daydaycook/hk/website/index.do")
    driver.maximize_window() # 放大視窗，因為首頁跑比較久，用來確認是否跑完
    # 避免廣告
    try:
        button = driver.find_element(By.ID, "ats-interstitial-button")
        button.click() # 關掉廣告
    except:
        pass # 沒有廣告沒事

    # 因為選擇料理時間、食譜排序後，之前輸入的食材有可能不見(?)，所以先按下搜索鍵進入篩選條件的畫面
    # driver.find_element(By.CLASS_NAME, "icon-btn_search").click() 
    driver.get("https://www.daydaycook.com/daydaycook/hk/website/recipe/search.do")
    # 避免廣告
    try:
        button = driver.find_element(By.ID, "ats-interstitial-button")
        button.click() # 關掉廣告
    except:
        pass # 沒有廣告沒事

    # 此時才輸入食材
    driver.find_element(By.ID, "searchText").send_keys(f"{material}")
    #driver.find_element(By.ID, "ats-interstitial-container").click() # 按下搜索鍵
    driver.find_element(By.CLASS_NAME, "icon-btn_search").click()
    # 以最高瀏覽次數排序
    driver.find_element(By.CSS_SELECTOR, " dd[onclick=\"searchRecList('sortKey','clickCount')\"]").click()

    # 抓取前5名的食譜：圖片、食譜名、食材、時間
    # 寫成函數，匯出dataframe
    links=driver.find_elements(By.CSS_SELECTOR, "#result>div:nth-child(2)>div>a")  #獲取到所有box標籤，組成一個列表
    url_lst = []
    for r in range(len(links)):
        url_lst.append(links[r].get_attribute('href'))

    # 抓取img的url正規表示式
    comment = re.compile(r'\"(http.*)\"') 
    title_lst = []
    time_lst = []
    watch_lst = []
    img_lst = []
    material_lst = []
    step_lst = []
    look_lst = []
    html_lst = []
    video_or_photo = []
    # 決定要抓幾個
    if recipe_len > len(url_lst):
        recipe_len = len(url_lst)
    print(recipe_len)
    for url in url_lst[:recipe_len]:
        html_lst += [url]
        slep = random.choice([1, 3, 4])
        time.sleep(slep)
        driver.get(url) 
        try: # 是影片
            if driver.find_element(By.ID, "video"):
                print("video")
                video_or_photo += ['有影片']
                string = driver.find_element(By.CLASS_NAME, "vjs-poster").get_attribute('style')
                # 抓取url
                img_url = comment.findall(string)
                if 'https' not in img_url:
                    img_url = img_url.replace('http', 'https')
                img_lst += img_url
                # 烹飪所需時間
                try:
                    times = driver.find_element(By.CLASS_NAME, "timeLen").text.split(':')[1]
                except:
                    times = '未知'
                time_lst += [times]
                # 觀看數
                look = driver.find_element(By.CLASS_NAME, 'lookLen').find_element(By.CLASS_NAME, 'txt').text
                look_lst += [int(look)]
                # 去食材的網頁
                temp_url = driver.find_element(By.CSS_SELECTOR, "#video>div:nth-child(2)>div:nth-child(1)>div:nth-child(4)>a").get_attribute('href')
                driver.get(temp_url)
                # 食譜標題
                title = driver.find_element(By.CLASS_NAME, 'title').text
                title_lst.append(title)
                # 需要食材及份量，使用json格式儲存
                # (更新)改成計算數量，因此使用int格式儲存
                material = driver.find_element(By.CLASS_NAME, 'meterial').find_element(By.CLASS_NAME, 'info_b').text
                material_dict = dict()
                for x in material.split('\n'):
                    temp_string = x.split(' ')
                    material_dict[temp_string[0]] = temp_string[1]
                material_lst += [len(material_dict)]
                # 步驟，也是儲存成dict
                # (更新)改成計算數量，因此使用int格式儲存
                step = driver.find_element(By.CLASS_NAME, 'step').find_element(By.CLASS_NAME, 'info_b').text
                step_dict = dict()
                for x in step.replace('；','').split('\n'):
                    temp_string = x.split('.')
                    step_dict[temp_string[0]] = temp_string[1]
                step_lst+=[len(step_dict)]
        except: # 是圖片
            if driver.find_element(By.ID, "video"):
                print("pic")
                video_or_photo += ['純照片']
                # 抓取url
                img_url = driver.find_element(By.CSS_SELECTOR, "#video>div:nth-child(1)>img").get_attribute('src')
                if 'https' not in img_url:
                    img_url = img_url.replace('http', 'https')
                img_lst += [img_url]
                # 烹飪所需時間
                try:
                    times = driver.find_element(By.CLASS_NAME, "timeLen").text.split(':')[1]
                except:
                    times = '未知'
                time_lst += [times]
                # 觀看數
                look = driver.find_element(By.CLASS_NAME, 'lookLen').find_element(By.CLASS_NAME, 'txt').text
                look_lst += [int(look)]
                # 去食材的網頁
                temp_url = driver.find_element(By.CSS_SELECTOR, "#video>div:nth-child(2)>div:nth-child(1)>div:nth-child(4)>a").get_attribute('href')
                driver.get(temp_url)
                # 食譜標題
                title = driver.find_element(By.CLASS_NAME, 'title').text
                title_lst.append(title)
                # 需要食材及份量，使用json格式儲存
                # (更新)改成計算數量，因此使用int格式儲存
                material = driver.find_element(By.CLASS_NAME, 'meterial').find_element(By.CLASS_NAME, 'info_b').text
                material_dict = dict()
                for x in material.split('\n'):
                    temp_string = x.split(' ')
                    material_dict[temp_string[0]] = temp_string[1]
                material_lst += [len(material_dict)]
                # 步驟，也是儲存成dict
                # (更新)改成計算數量，因此使用int格式儲存
                step = driver.find_element(By.CLASS_NAME, 'step').find_element(By.CLASS_NAME, 'info_b').text
                step_dict = dict()
                for x in step.replace('；','').split('\n'):
                    temp_string = x.split('.')
                    step_dict[temp_string[0]] = temp_string[1]
                step_lst+=[len(step_dict)]
    driver.quit()
    print(img_lst)
    recipe_dict = {'food_name':title_lst, 'food_image':img_lst, 'look':look_lst, 'time':time_lst, 'type':video_or_photo, 'material':material_lst, 'method':step_lst, 'url':html_lst}
    recipe_df = pd.DataFrame.from_dict(recipe_dict,orient='index')
    return recipe_df#.to_dict('index')

#%%
'''
from DailyCook import DailyCook
df = DailyCook("南瓜", 5)
df = DailyCook("青椒", 5)
'''


