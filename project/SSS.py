from bs4 import BeautifulSoup
from selenium import webdriver
from pymongo import MongoClient
import re
from DB_Info import db_info
def extract_smarts():
    url = "https://e-onestop.pusan.ac.kr/menu/bbs/notice/list?menuId=20001104&rMenu=12"
    options = webdriver.ChromeOptions()
    options.headless = True

    browser = webdriver.Chrome(
        r"C:\chromedriver\chromedriver", options=options)
    browser.get(url)

    soup = BeautifulSoup(browser.page_source, 'html.parser')
    results = soup.find('table', attrs={'id': 'bbs'}).find(
        'tbody').find_all('tr')

    smarts = []
    for result in results:
        datas = result.find_all('td')

        title = datas[1].a.get_text().strip()
        rate = datas[2].get_text().strip().replace('-', '.')
        link_index = re.findall("\\d+",datas[1].a['onclick'])[0]
        link = f"https://e-onestop.pusan.ac.kr/menu/bbs/notice/view?bbsConfNo=1&articleNo={link_index}&menuId=20001104&rMenu=12"
        smart = {'title': title, 'rate': rate, 'link': link}
        client = MongoClient(db_info())
        db = client.Board_DB
        collection = db.SSS_Collection
        collection.update(smart,smart,upsert=True)

        smarts.append(
            {'title': title, 'rate': rate, 'link': link}
        )

    browser.quit()


def get_smarts():
    extract_smarts()
