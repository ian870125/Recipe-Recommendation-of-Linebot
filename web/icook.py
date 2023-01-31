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
from selenium.webdriver.chrome.options import Options
import os
# import wget
import requests
from urllib.request import urlopen
import urllib
import random
import numpy as np
import nums_from_string as nfs


def crawer(keyword, number):
    # 連到愛料理
    driver = webdriver.Chrome(ChromeDriverManager().install())
    #options = Options()
    #options.chrome_executable_path = "D:/recipe/web/chromedriver.exe"
    #driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    time.sleep(3)

    #輸入關鍵字
    driver.get(f"https://icook.tw/search/食材：{keyword}")

    recipe = {}

    # 最多只能抓18道料理(第一頁內容)
    if number <= 18:
        number= number
    else:
        number = 18

    for i in range(number):
        # 料理網址
        dish_url = driver.find_elements(By.CLASS_NAME, 'browse-recipe-link')[i].get_attribute('href')


        # 點擊
        dishes = driver.find_elements(By.CLASS_NAME, 'browse-recipe-name')
        dishes[i].click()


        # 料理名稱
        recipe_name = driver.find_element(By.CLASS_NAME, 'title').text


        # 圖片
        img_url = driver.find_element(By.CSS_SELECTOR,
                                      "#o-wrapper > div:nth-child(7) > div.row.row--flex > main > article > div.recipe-details > div.recipe-details-header.recipe-details-block > div > div.header-col.left-col > div > a > img").get_attribute(
            'src')


        # 讚數
        good = driver.find_element(By.CLASS_NAME, 'stat-content').text


        # 點擊數/收藏數
        seen = driver.find_element(By.CLASS_NAME, 'recipe-detail-metas')
        seen_content = seen.text.split(' ')


        # 烹飪時間
        try:
            minute = (driver.find_elements(By.CLASS_NAME, 'info-content'))[1].text
        except:
            minute = '未知'


        # 食材數
        ingredients = driver.find_elements(By.CLASS_NAME, 'ingredient-search')
        number_of_ingredients = len(ingredients)


        # 步驟數
        steps_description = driver.find_elements(By.CLASS_NAME, 'recipe-step-description-content')
        number_of_steps = len(steps_description)


        recipe_dict = {'food_name': recipe_name, 'food_image': img_url, 'look': seen_content[0], 'time': minute,'good': nfs.get_nums(good)[0],
                        'material': number_of_ingredients, 'method': number_of_steps, 'url': dish_url}
        recipe[str(i)] = recipe_dict


        driver.back()
    driver.close()
    return pd.DataFrame(recipe)




















