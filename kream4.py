from selenium import webdriver # 셀레니움이라는 라이브러리에서 웹드라이버 모듈을 찾아서 링크(참조)하는 것
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import re
import json
from bs4 import BeautifulSoup
# 키보드 관련 동작과 기능을 쓰기위한 패키지
from selenium.webdriver.common.keys import Keys
# 클래스, 아이디, css_selector 를 위한 패키지
from selenium.webdriver.common.by import By
# Mysql 연동을 위한 패키지
from pymongo import MongoClient

# MongoDB 인스턴스에 연결
client = MongoClient('mongodb://localhost:27017')

db = client['DataBase']
collection = db['kream']

# 크롤링을 위한 기본세팅
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

options = Options()
options.add_argument(f"user-agent={user_agent}")
options.add_experimental_option('detach', True)
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_experimental_option('excludeSwitches', ['enable-automation'])

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

url = "https://kream.co.kr/"
driver.get(url)
time.sleep(0.5)

#더보기 버튼이 크롤링할 부분에 존재하면 클릭하도록 하는 반복문
while True :
    try :
        driver.find_element(By.XPATH, '//*[@id="wrap"]/div[4]/div[3]/div[2]/div[9]/div[2]/div[2]/a').click()
        time.sleep(0.5)
    except :
        break

item_area = driver.find_element(By.XPATH,'//*[@id="wrap"]/div[4]/div[3]/div[2]/div[9]/div[2]/div[1]')
items= item_area.find_elements(By.CSS_SELECTOR, '.product_item')
crawl_data = []
#반복문을 통해 크롤링 데이터 수집
for i in items :
    product_name = i.find_element(By.CSS_SELECTOR, ".name").text
    if ']' in product_name :
        product_name = product_name.split(']')[1]
    brand = i.find_element(By.CSS_SELECTOR, ".brand-text").text
    price_text = i.find_element(By.CSS_SELECTOR, ".amount.lg > .num").text
    price = ''.join(filter(str.isdigit, price_text))
    if ('Women' in product_name) or ('(W)' in product_name):
        gender = 'female'
    else :
        gender = 'unisex'
    category = None
# 데이터를 MongoDB에 추가하는 부분
    temp = { "category" : category, "brand" : brand, "product" : product_name, "price" : price, "gender" : gender }
    crawl_data.append(temp)

collection.insert_many(crawl_data)
    

# MongoDB에서 가져온 데이터를 넣을 딕셔너리
data = {
    "title" : "KREAM_Crawling",
    "description" : "파이썬, selenium을 활용한 크림 크롤링 데이터",
    "items" : []
}

# MongoDB에서 데이터 가져오기
# sql = ({}, {category : 1, brand : 1, product : 1, price : 1, gender : 1})
mongoDB_data = collection.find({}, {'_id': 0})
for i in  mongoDB_data:
    data["items"].append(i)
    
# 크롤링한 데이터를 파일화
with open('crawled_data.json', 'w') as file:
    json.dump(data, file)
    print('json 파일화 성공')
driver.quit()