# -*- coding: utf-8 -*-
"""
Created on Mon Nov  1 14:32:44 2021

@author: Regan Yue@EddieHub
"""

import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import time
import numpy as np
from PIL import Image
import jieba
import wordcloud

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36 FS"}

video_time=[]
abstime=[]
userid=[]
comment_content=[]

def get_cid(url):
    data = requests.get(url=url,headers=headers)
    data = data.json()
    cid = data['data'][0]['cid']
    return cid

def get_info(url):
    html = requests.get(url=url, headers=headers)
    html.encoding = html.apparent_encoding
    
    soup = BeautifulSoup(html.text,'lxml')
    
    data_number=re.findall('d p="(.*?)">',html.text)
    data_text=re.findall('">(.*?)</d>',html.text)
    
    comment_content.extend(data_text)
    for each_numbers in data_number:
        
        each_numbers=each_numbers.split(',')
        
        video_time.append(each_numbers[0])           
        abstime.append(time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(int(each_numbers[4]))))      
        userid.append(each_numbers[6])
        
    result={'用户id':userid,'评论时间':abstime,'视频位置(s)':video_time,'弹幕内容':comment_content}
    results=pd.DataFrame(result)
    final= results.drop_duplicates()
    final.info()
    final.to_excel('B站弹幕.xls')

def getWord(text):
    cut_txt = jieba.cut(text)
    result = " ".join(cut_txt)
    print(result[:30])
    return result

def setWordCloud():
    pic = np.array(Image.open("./cat.jpg"))
    stopwords = set(wordcloud.STOPWORDS)
    stopwords.add("好")
    font = r".\妙笔生花.ttf"
    wc = wordcloud.WordCloud(
            font_path=font,
            background_color="white", 
            max_words=1000, 
            mask=pic,
            stopwords=stopwords,
            max_font_size=30,
            random_state=45
        )
    return wc

def getWordCloud(wc,result):
    wc.generate(result)
    wc.to_file("./wordcloud.jpg")
    
def main():
    url = "https://www.bilibili.com/video/BV1aJ411C7tb/?spm_id_from=autoNext"
    cid_url = "https://api.bilibili.com/x/player/pagelist?bvid="+str(url[31:43]) +"&jsonp=jsonp"
    cid = get_cid(cid_url)
    oid_url = 'https://api.bilibili.com/x/v1/dm/list.so?oid='+str(cid)
    get_info(oid_url)
    
    content = " ".join(comment_content)
    word = getWord(content)
    wc = setWordCloud()
    getWordCloud(wc, word)
    
main()