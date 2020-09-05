import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from DB_Info import db_info

LIMIT = 50
URL = "http://www.busanit.or.kr/board/list.asp?bcode=notice_e&sword=&search_txt=&ipage="

client = MongoClient(db_info())
db = client.Board_DB
collection = db.INFO_IND_Collection

def extract_busanit(html,num):
    title = html.find("td",{"class":"subject"}).find('a')["title"].strip()
    rate = list(html.find_all("td",recursive = False))[2].string
    view = list(html.find_all("td",recursive = False))[3].string
    link = html.find("td",{"class":"subject"}).find('a')["href"]
    return {
        "title":title,
        "rate":rate.replace("-","."),
        "view":view,
        "link":f"http://www.busanit.or.kr/board/{link}"
    }


def extract_busanits():
    busanits = []
    
    for page in range(5):
        
        print(f"Scrapping busanit : Page:{page+1}")
        result = requests.get(f"{URL}{page + 1}")
        soup = BeautifulSoup(result.content.decode('UTF-8','replace'), 'html.parser')
        results = soup.find("div",{"class":"content_sub"}).find("table", {"class":"bbs_ltype"}).find("tbody").find_all("tr")
        i = 1
        for result in results:
            busanit = extract_busanit(result,i)
            collection.update(busanit,busanit,upsert=True)
            busanits.append(busanit)
            i+=1
   

def get_busanits():
  extract_busanits()


#def save_to_file(busanits):
#  file = open("busanit.csv", mode = 'w',encoding = "UTF-8-sig")
#  writer = csv.writer(file)
#  writer.writerow(["title", "rate", "file", "link"])
#  for busanit in busanits:
#    writer.writerow(list(busanit.values()))
#    print(busanit)
    
#  return

#busanits = get_busanits()
#save_to_file(busanits)