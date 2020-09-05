from selenium import webdriver
from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.keys import Keys
import requests
import time 
import os, sys
from bs4 import BeautifulSoup
from selenium import webdriver
from pymongo import MongoClient
from DB_Info import db_info

client = MongoClient(db_info())
db = client.Board_DB
collection1 = db.Youtube_Collection
collection2 = db.Youtube_Collection2
collection3 = db.Youtube_Collection3



def get_vid(search_word) :
    options = webdriver.ChromeOptions()
    options.headless = True
    driver = webdriver.Chrome(r"C:\chromedriver\chromedriver", options=options)
    URL = f"https://www.youtube.com/results?search_query={search_word}&sp=CAMSAhAB"
    driver.get(URL)

    last_page_height = driver.execute_script("return document.documentElement.scrollHeight")
    count = 0
    while(True and count < 3):
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);") 
        time.sleep(3.0)
        new_page_height = driver.execute_script("return document.documentElement.scrollHeight") 
        last_page_height = new_page_height
        count = count + 1
        if new_page_height == last_page_height: 
            break
    soup = bs(driver.page_source, 'html.parser')
    videos = get_info(soup, search_word)
    driver.close()
    return videos

def get_info(soup, search_word):
    rows = soup.find_all('ytd-video-renderer')
    videos = []
    for row in rows:
        video_anchor = row.find('a', {"id":"video-title"})
        video_title = video_anchor.get("title")
        video_url = (video_anchor.get("href").replace("/watch?v=",""))
        video_length = row.find('span',{"class":"style-scope"}).string
        get_views = row.find('span', {"class": "style-scope ytd-video-meta-block"}).string.split()[0]
        if video_length is not None:
            video_length = video_length.split()
            length = ""
            video_length = length.join(video_length)
            one_video = {'title' : video_title, 
                                 'views' : get_views, 
                                 'video length' : video_length ,
                                 "url": f"https://www.youtube.com/embed/"+video_url}
            
            if len(video_length)==4:
                if search_word == "공부 동기부여":
                    collection1.update(one_video,one_video,upsert=True)
                if search_word == "취업 팁":
                    collection2.update(one_video,one_video,upsert=True)    
                if search_word == "코딩테스트":
                    collection3.update(one_video,one_video,upsert=True)
                videos.append(one_video)
    return videos
"""
    #not used
    def get_views()
    if get_views[len(get_views)-1]=='M':
        print("High")
    elif get_views[len(get_views)-1]=='K':
        get_views = get_views[:-1]
        if(int(get_views)>100):
            print("over")
        else:
            break
        else:
            break
        print(get_views)
    return
"""
"""
def save_to_file(search_word):
    file = open(f"{search_word}.csv",mode="w",buffering=-1,encoding="utf-8")
    writer = csv.writer(file)
    writer.writerow(["title, company, location, link"])
    videos = get_last_page(search_word)
    print(videos)
    for video in videos:
        writer.writerow(list(video.values()))
    return 
"""