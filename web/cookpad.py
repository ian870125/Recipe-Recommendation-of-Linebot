#!/usr/bin/env python
# coding: utf-8

# In[9]:


import requests
from bs4 import BeautifulSoup 
from fake_useragent import UserAgent
import time
import pandas as pd
import random
import re
import nums_from_string as nfs
def scrape(keyword, n):
    scrap = {}
    ua = UserAgent()
    user_agent = ua.random
    key = ''
    for keykey in keyword:
        key+keykey


    u = "https://cookpad.com/tw/%E6%90%9C%E5%B0%8B/" + key +"?event=search.history"
    headers = {'User-Agent': user_agent, 'Referer': 'https://cookpad.com/tw/%E6%90%9C%E5%B0%8B/%E7%89%9B%E8%82%89?event=search.typed_query'}
    response = requests.get(u, headers=headers)
    print(response)
    soup = BeautifulSoup(response.content, "html.parser")
    cards = soup.find_all('li', {'class': 'block-link card border-cookpad-gray-400 border-t-0 border-l-0 border-r-0 border-b flex m-0 rounded-none overflow-hidden ranked-list__item xs:border-b-none xs:mb-sm xs:rounded'}, limit=n)

    for card in cards:
        title = card.find("a", {"class": "block-link__main"}).getText()
        title = title.replace('/', '-')
        title = title.strip()
        if 'title' not in scrap.keys():
            scrap['title'] = [title]
        else:
            scrap['title'].append(title)
        try:
            url = card.find("a")
            url = 'https://cookpad.com' + url["href"]
            if 'url' not in scrap.keys():
                scrap['url'] = [url]
            else:
                scrap['url'].append(url)
        except:
            url = 'https://cookpad.com'
            if 'url' not in scrap.keys():
                scrap['url'] = ['']
            else:
                scrap['url'].append('')
            continue

        try:
            img_url = card.find('source', {'type': 'image/webp'}).get('data-srcset').split(',')[1]
            if 'picture' not in scrap.keys():
                scrap['picture'] = [img_url]
            else:
                scrap['picture'].append(img_url)
        except:
            if 'picture' not in scrap.keys():
                scrap['picture'] = ['']
            else:
                scrap['picture'].append('')
        try:
            ti = card.find_all('li', {'class': 'inline mr-rg'})[0].getText().replace('\n', '')
            if 'cooking_time' not in scrap.keys():
                scrap['cooking_time'] = [ti]
            else:
                scrap['cooking_time'].append(ti)
        except:
            if 'cooking_time' not in scrap.keys():
                scrap['cooking_time'] = ['']

            else:
                scrap['cooking_time'].append('')

        try:
            quantity = card.find_all('li', {'class': 'inline mr-rg'})[1].getText().replace('\n', '')
            if 'quantity' not in scrap.keys():
                scrap['quantity'] = [int(nfs.get_nums(quantity)[1])]
            else:
                scrap['quantity'].append(int(nfs.get_nums(quantity)[1]))
        except:
            if 'quantity' not in scrap.keys():
                scrap['quantity'] = ['']
            else:
                scrap['quantity'].append('')

        try:
            ingrediant = card.find('div', {'class': 'clamp-2 break-words'}).getText().replace('\n', '')

            if 'ingrediant' not in scrap.keys():
                scrap['ingrediant'] = [len(ingrediant.split('•'))-1]
            else:
                scrap['ingrediant'].append(len(ingrediant.split('•'))-1)
        except:
            if 'ingrediant' not in scrap.keys():
                scrap['ingrediant'] = ['']
            else:
                scrap['ingrediant'].append('')
    for i in scrap['url']:
        ua = UserAgent()
        user_agent = ua.random
        headers = {'User-Agent': user_agent, 'referer':i}
        time.sleep(random.choice([5, 7, 10]))
        response = requests.get(i, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        print(response)
        try:
            great = soup.find_all('span', {'data-reactions-target': 'count'})
            if 'great' not in scrap.keys():
                scrap['great'] = [sum([int(i.text) for i in great])]
            else:
                scrap['great'].append(sum([int(i.text) for i in great]))
        except:
            if 'great' not in scrap.keys():
                scrap['great'] = [0]
            else:
                scrap['great'].append(0)
    return pd.DataFrame(scrap)


# In[ ]:
