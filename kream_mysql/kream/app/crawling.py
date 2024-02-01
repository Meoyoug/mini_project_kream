from selenium import webdriver # 셀레니움이라는 라이브러리에서 웹드라이버 모듈을 찾아서 링크(참조)하는 것
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
# 키보드 관련 동작과 기능을 쓰기위한 패키지
from selenium.webdriver.common.keys import Keys
# 클래스, 아이디, css_selector 를 위한 패키지
from selenium.webdriver.common.by import By
# Mysql 연동을 위한 패키지
import pymysql


# MySQL 연동을 위한 세팅
connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='eodyd456@',
                                 db='kream_new_product',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

def execute_query(connection, query, args=None):
    with connection.cursor() as cursor:
        cursor.execute(query, args or ())
        if query.strip().upper().startswith('SELECT'):
            return cursor.fetchall()
        else:
            connection.commit()
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

# 카테고리와 성별 데이터를 얻어오는 함수
def get_category (arg):
    driver.find_element(By.CSS_SELECTOR, '.btn_search').click()
    for val in arg :
        driver.find_element(By.CSS_SELECTOR, '.input_search').send_keys(val["product"])
        time.sleep(0.5)
        driver.find_element(By.CSS_SELECTOR, '.input_search').send_keys(Keys.RETURN)
        time.sleep(0.5)
        val["category"] = driver.find_element(By.XPATH,'//*[@id="__layout"]/div/div[3]/div[3]/aside/div/div[3]/div[2]/ul/li/p').get_attribute('textContent')
        try :
            if driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[3]/div[3]/aside/div/div[4]/div/div[1]/span[1]').text == '성별':
                driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[3]/div[3]/aside/div/div[4]/div/div[1]/span[1]').click()
                gender_area = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[3]/div[3]/aside/div/div[4]/div[2]/ul/li/ul').text
                gender_text = ''.join([char for char in gender_area if '가' <= char <= '힣'])
                if '남' in gender_text :
                    val["gender"] = 'male'
                    if '여' in gender_text :
                        val["gender"] = 'unisex'
                        if '키즈' in gender_text :
                            val["gender"] += ', kids'
                elif '여' in gender_text :
                    val["gender"] = 'female'
                    if '키즈' in gender_text :
                        val["gender"] += ', kids'
                elif '키즈' in gender_text :
                    val["gender"] = 'kids'
            else : 
                val["gender"] = None
        except :
            val["gender"] = None

        driver.refresh()
        driver.find_element(By.CSS_SELECTOR, '.input_search').clear()


#반복문을 통해 크롤링 데이터 수집
crawl_data =[]
for i in items :
    product_name = i.find_element(By.CSS_SELECTOR, ".name").text
    if ']' in product_name :
        product_name = product_name.split(']')[1]
    brand = i.find_element(By.CSS_SELECTOR, ".brand-text").text
    price_text = i.find_element(By.CSS_SELECTOR, ".amount.lg > .num").text
    price = ''.join(filter(str.isdigit, price_text))
    if not price :
        price = None
    img = i.find_element(By.CSS_SELECTOR, '.product_img > .full_width').get_attribute('src')
    kr_description = i.find_element(By.CSS_SELECTOR, '.product_img > .full_width').get_attribute('alt')
    product_link = i.find_element(By.CSS_SELECTOR, '.item_inner').get_attribute('href')
    data = {
        "brand" : brand,
        "product" : product_name,
        "price" : price,
        "img" : img,
        "product_link" : product_link,
        "kr_description" : kr_description
    }
    crawl_data.append(data)
# get_category 함수를 호출해서  crawl_data의 성별과 카테고리를 업데이트
get_category(crawl_data)


# 데이터를 MySQL에 추가하는 부분
sql = "INSERT INTO products (category, brand, product, price, gender, img, product_link, kr_description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
for i in crawl_data :
    try :
        execute_query(connection, sql, (i["category"], i["brand"], i["product"], i["price"], i["gender"], i["img"], i["product_link"], i["kr_description"]))
        print('데이터 추가 성공')
    except pymysql.IntegrityError as e :
        print(f'Error: {e}')
        print('UNIQUE 조건에 따라 데이터를 추가하지 않습니다.')
        print('다음 데이터 추가를 시도합니다.')
        continue

driver.close()