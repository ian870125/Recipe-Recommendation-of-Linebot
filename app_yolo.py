## https://ithelp.ithome.com.tw/articles/10279933

from flask import Flask, request, abort

#https://pypi.org/project/line-bot-sdk/
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import re

import pandas as pd
import urllib.request
import json
from kitchen_story import *
from googletrans import Translator
import cv2 as cv
import torch 
torch.hub.set_dir('D:/課程學習/政大課程/研究所課程/統計諮詢/linebot/food-recognition/yolov5')
#from linebot.models.send_messages import ImageSendMessage

#from moon import *

app = Flask(__name__)


# 必須放上自己的Channel Access Token(在line那邊按下issue)
line_bot_api = LineBotApi('')
#message_content = line_bot_api.get_message_content('<message_id>')


# 必須放上自己的Channel Secret
handler = WebhookHandler('')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent) #, message=TextMessage
def handle_message(event):

    if (event.message.type == "image"):
        
        #event.contentProvider.originalContentUrl
        model = torch.hub.load('ultralytics/yolov5', 'yolov5l')  # yolov5n - yolov5x6 or custom
        image_content  = line_bot_api.get_message_content(event.message.id)
 
        
        path='./img/test.jpg'
        with open(path, 'wb') as fd:
            for chunk in image_content.iter_content():
                fd.write(chunk)
                
        results = model(cv.imread('./img/test.jpg',1)) 
        img_corp = results.crop()
        keyword = list(set([img_corp[i]['label'].split(" ")[0] for i in range(len(img_corp)) if img_corp[i]['label'].split(" ")[0] not in (['bowl','cup','dining','spoon','sandwich'])]))
        
        translator = Translator() 
        keyword = [translator.translate(i, dest='zh-TW').text for i in keyword]
        
    else : 
        keyword=event.message.text
        
    # keyword=event.message.text

    #line_bot_api.reply_message(
     #   event.reply_token,
      #  TextSendMessage(text="等我一下 我找一下"+event.message.text+"食譜"))
    
    if type(keyword)==list:
        data=get_food_info(5,keyword)
    else :
        data=get_food_info(5,[keyword])
    # data=get_food_info(5,keyword)
    food_name=data['Name'][0]
    food_material=data['ingredients'][0]
    food_image=data['img'][0]
    food_method=data['steps'][0]
    food_url=data["URL"][0]
    # line_bot_api.reply_message(
    #      event.reply_token,
    #      TextSendMessage(text=food_url))
    carousel_template_message = TemplateSendMessage(
        alt_text='Carousel template',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url=food_image,
                    title=str(food_name),
                    # text = str(keyword),
                    text=f'{keyword} - 準備材料與做法:...',
                    actions=[
                        URIAction(
                            label='點我看更多',
                            uri=food_url
                        )
                    ]
                )
            ]
        )
    )
    

    line_bot_api.reply_message(event.reply_token, carousel_template_message)


if __name__ == "__main__":
    app.debug=True
    app.run()
    
    
## https://ithelp.ithome.com.tw/articles/10279953?sc=iThomeR