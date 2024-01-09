from selenium import webdriver
from bs4 import BeautifulSoup
import time
import json
header_user = {
    "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

url = "https://kream.co.kr/exhibitions/2082"

driver = webdriver.Chrome()
driver.get(url)
for i in range(5) : 
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

html = driver.page_source
soup = BeautifulSoup(html, "html.parser")
total_area = soup.select(".product_card.exhibition_product")
if total_area : 
    areas = total_area
else : 
    print("클래스 명 변경 필요")


index = 1
# json 데이터 생성하기.
data = {
    "title" : "KREAM_Crawling",
    "description" : "파이썬, selenium을 활용한 크림 크롤링 데이터",
    "items" : []
}
for i in total_area :
    current_price = i.select_one(".amount")
    brand = i.select_one(".product_info_brand.brand")
    name = i.select_one(".translated_name")
    #category = i.select_one(".style-code")
    #크롤링한 데이터를 json 데이터에 추가.
    addItem = {"category": "", "brand": f"{brand.text}", "product": f"{name.text}", "price": f"{current_price.text}", "gender": ""}
    data['items'].append(addItem)
    # print(f"[{index}]")
    # print(f"브랜드 : {brand.text}")
    # print(f"제품명 : {name.text}")
    # print(f"가격 : {current_price.text}")
    # print()
    index += 1
print(data)
with open('crawled_data.json', 'w') as file:
    json.dump(data, file)
