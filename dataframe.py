import pandas as pd
import numpy as np
import nums_from_string as nfs
import re
from web import cookpad,dailycook,icook,kitchen_story

def generate_data(keyword,number):
    def get_cookpad(keyword,number):
        try:
            return cookpad.scrape(keyword,number)
        except Exception:
            return pd.DataFrame()

    def get_dailycook(keyword,number):
        try:
            return dailycook.DailyCook(keyword,number)
        except Exception:
            return pd.DataFrame()

    def get_kitchen_story(number,keyword):
        try:
            return kitchen_story.get_food_info(number,keyword)
        except Exception:
            return pd.DataFrame()

    def get_icook(keyword,number):
        try:
            return icook.crawer(keyword,number)
        except Exception:
            return pd.DataFrame()

    cookpad_data = get_cookpad(' '.join(keyword),number)#擋爬蟲
    kitchen_story_data  = get_kitchen_story(number,' '.join(keyword))#支語
    dailycook_data = get_dailycook(''.join(keyword),number) #這個網站食譜較少
    icook_data = get_icook(' '.join(keyword),number)
    dailycook_data = dailycook_data.T
    icook_data = icook_data.T
    #註明食譜網站
    cookpad_data =  cookpad_data.assign(Website = 'cookpad')
    kitchen_story_data = kitchen_story_data.assign(Website = 'kitchen_story')
    dailycook_data = dailycook_data.assign(Website = '日日煮')
    icook_data = icook_data.assign(Website = '愛料理')
    #欄位重新命名
    cookpad_data = cookpad_data.rename(columns = {"title":'食譜名稱',"url":'url', "picture":'圖片連結', "cooking_time":'烹飪時間',
                 "ingrediant" :'食材種類', "quantity" :'烹飪步驟', "great" :'按讚數'})

    dailycook_data = dailycook_data.rename(columns = {"food_name":'食譜名稱'
    ,"url":'url', "food_image" :'圖片連結', "time" : '烹飪時間',
    "material" : '食材種類', "method" : '烹飪步驟',"look" : '點擊次數',"type":"有無影片"})

    icook_data = icook_data.rename(columns = {"food_name" : '食譜名稱' ,"url" : 'url', "food_image" : '圖片連結', "time" : '烹飪時間',
        "material" : '食材種類', "method" : '烹飪步驟', "look" : '點擊次數', "good" : '按讚數'})
    kitchen_story_data  = kitchen_story_data.rename(columns = {"Name" : '食譜名稱'
            ,"URL" : 'url', "img" : '圖片連結', "Time" : '烹飪時間',
            "ingredients" :'食材種類', "steps" : '烹飪步驟', "Like_num" : '按讚數',"Nutrition":"營養資訊","have_video":"有無影片"})

    #合併
    result = pd.DataFrame(columns=['食譜名稱','url','圖片連結','烹飪時間','食材種類','烹飪步驟','按讚數','點擊次數','有無影片','營養資訊'])
    frames = [cookpad_data,dailycook_data,icook_data,kitchen_story_data]
    result = pd.concat(frames)\
            .reset_index()
    result = result.iloc[:,1:11]
    result = result.fillna('None')
    result.烹飪時間.replace(['1小時','一個半小時','2 小時','None','VIP 限定功能 VIP 獨享','未知'],['60分鐘','90分鐘','120分鐘',0,0,0],inplace=True)
    for i in range(0,len(result.烹飪時間)):
        if isinstance(result.烹飪時間[i] , str):
            result.烹飪時間[i] = nfs.get_nums(result.烹飪時間[i])[0]
    #讀取楊桃資料庫
    yuntow = pd.read_excel("楊桃食譜資料庫.xlsx")
    yuntow.material = yuntow.material.map(lambda x: re.split('[.,]', x))
    yuntow_data = yuntow[yuntow.material.map(lambda x:sum([True for i in keyword for j in x if i in j]) == len(keyword))]
    yuntow_data = yuntow_data.iloc[:,[1,2,3,4,8,9]]
    yuntow_data = yuntow_data.rename(columns={"name":'食譜名稱',"image":'圖片連結',"url":'url',"like":'按讚數',"step_number":'烹飪步驟',"material_number":'食材種類'})
    yuntow_data = yuntow_data.assign(Website = '楊桃')
    data = pd.concat([result,yuntow_data])\
            .reset_index()
    #存成csv
    result.to_csv("results/results_{name}.csv".format(name=keyword),encoding="utf-8_sig")
    data.to_csv("results/data_{name}.csv".format(name=keyword),encoding="utf-8_sig")
    return data

#in[]
#data = generate_data('香菜',5)
"""
統一內容形式
beef = pd.read_csv("D:/recipe/results/results_牛肉_Origin.csv")
beef.烹飪時間 = beef.烹飪時間.fillna(0)
beef.烹飪時間.replace(['1小時','一個半小時','2 小時','None','VIP 限定功能 VIP 獨享','未知'],['60分鐘','90分鐘','120分鐘',0,0,0],inplace=True)
for i in range(0,len(beef.烹飪時間)):
    if isinstance(beef.烹飪時間[i] , str):
        beef.烹飪時間[i] = nfs.get_nums(beef.烹飪時間[i])[0]
import nums_from_string as nfs
number_list = nfs.get_nums(beef.烹飪時間)[0]
pork = pd.read_csv("D:/recipe/results/results_豬肉.csv")
int(pork.烹飪步驟[3][1])
"""