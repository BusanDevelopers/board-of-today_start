from CSE_Notice import get_notices
from INFO_IND import get_busanits
from EMP import get_emps
from SSS import get_smarts
from pymongo import MongoClient
from youtube import get_vid
get_emps()
get_notices()
get_busanits()
get_smarts()
videos1 = get_vid("공부 동기부여")
videos2 = get_vid("취업 팁")
videos3 = get_vid("코딩테스트")









