import requests
from bs4 import BeautifulSoup
import csv
from pymongo import MongoClient

LIMIT = 50
URL1 = f"https://cse.pusan.ac.kr/cse/14651/subview.do?enc=Zm5jdDF8QEB8JTJGYmJzJTJGY3NlJTJGMjYwNSUyRmFydGNsTGlzdC5kbyUzRmJic09wZW5XcmRTZXElM0QlMjZpc1ZpZXdNaW5lJTNEZmFsc2UlMjZzcmNoQ29sdW1uJTNEJTI2cGFnZSUzRD"
URL2 = f"lMjZzcmNoV3JkJTNEJTI2cmdzQmduZGVTdHIlM0QlMjZiYnNDbFNlcSUzRCUyNnJnc0VuZGRlU3RyJTNEJTI2"

client = MongoClient()
db = client.Board_DB
collection = db.CSE_Notice_Collection

def extract_notice(html, num):
    title = html.find("td",{"class":"_artclTdTitle"}).find('a').find("strong").string 
    rate = html.find("td",{"class":"_artclTdRdate"}).string.strip()
    file = html.find("td",{"class":"_artclTdAtchFile"}).string.strip()
    link = html.find("td",{"class":"_artclTdTitle"}).find('a')["href"]
    return {
        "title":title,
        "rate":rate,
        "file":file,
        "link":f"https://cse.pusan.ac.kr{link}"
    }


def extract_notices():
    notices = []
    
    for page in range(5):
        page_alphabet = chr(69 + page*4)
        print(f"Scrapping Notice : Page:{page}")
        result = requests.get(f"{URL1}{page_alphabet}{URL2}")
        soup = BeautifulSoup(result.text, 'html.parser')
        results = soup.find("table",{"class":"artclTable artclHorNum1"}).find("tbody").find_all("tr")
        i = 1
        for result in results:
            if result.find("td",{"class":"_artclTdNum"}).string != None:
                notice = extract_notice(result, i)
                collection.update(notice,notice,upsert=True)
                notices.append(notice)
                i+=1
    



def get_notices():
  extract_notices()

#def save_to_file(notices):
#  file = open("notice.csv", mode = 'w',encoding = "CP949")
#  writer = csv.writer(file)
#  writer.writerow(["title", "rate", "file", "link"])
#  for notice in notices:
#    writer.writerow(list(notice.values()))
#    print(notice)

#  return

#notices = get_notices()
#save_to_file(notices)