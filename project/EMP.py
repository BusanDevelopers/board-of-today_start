import requests 
from bs4 import BeautifulSoup 
from pymongo import MongoClient
pageChar = 100
from DB_Info import db_info

URL = f"https://cse.pusan.ac.kr/cse/14667/subview.do?enc=Zm5jdDF8QEB8JTJGYmJzJTJGY3NlJTJGMjYxNiUyRmFydGNsTGlzdC5kbyUzRmJic09wZW5XcmRTZXElM0QlMjZpc1ZpZXdNaW5lJTNEZmFsc2UlMjZzcmNoQ29sdW1uJTNEJTI2cGFnZSUzRD{chr(pageChar)}lMjZzcmNoV3JkJTNEJTI2cmdzQmduZGVTdHIlM0QlMjZiYnNDbFNlcSUzRCUyNnJn"

#def get_last_pages():
#  result = requests.get(URL)
#  soup = BeautifulSoup(result.text, "html.parser")
#  pagination = soup.find("div", {"class":"s-pagination"})
#  links = pagination.find_all('a')

#  last_page = links[-2].get_text(strip=True)
#  return int(last_page)
client = MongoClient(db_info())
db = client.Board_DB
collection = db.EMP_Collection

def extract(html, html2, num):
    
    title = html.find("strong").string
    link = html.find("a")["href"]
    date = html2.string
    return {"title": title,"date": date, "link": f"http://cse.pusan.ac.kr{link}"}

def extracts():
  emps = []
  pageChar = 65
  
  for page in range(5):
   pageChar += 4
   print(f"Scrapping emp {page+1} page")
   result = requests.get(f"https://cse.pusan.ac.kr/cse/14667/subview.do?enc=Zm5jdDF8QEB8JTJGYmJzJTJGY3NlJTJGMjYxNiUyRmFydGNsTGlzdC5kbyUzRmJic09wZW5XcmRTZXElM0QlMjZpc1ZpZXdNaW5lJTNEZmFsc2UlMjZzcmNoQ29sdW1uJTNEJTI2cGFnZSUzRD{chr(pageChar)}lMjZzcmNoV3JkJTNEJTI2cmdzQmduZGVTdHIlM0QlMjZiYnNDbFNlcSUzRCUyNnJn")
  
   soup = BeautifulSoup(result.text, "html.parser")
   results = soup.find_all("td", {"class":"_artclTdTitle"})
   results2 = soup.find_all("td", {"class":"_artclTdRdate"})
   results3 = soup.find_all("td", {"class":"_artclTdNum"})
   num = 1
   i = 0
   for result3 in results3:
      if result3.string != None:
        emp = extract(results[i], results2[i], num)
        collection.update(emp,emp,upsert=True)
        emps.append(emp)
        num += 1
 
        
      i+=1

def get_emps():
  #last_page = get_last_pages()
  extracts()
