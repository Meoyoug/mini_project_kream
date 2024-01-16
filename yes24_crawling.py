from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
import time
import pymysql

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

options = Options()
options.add_argument(f"user-agent={user_agent}")
options.add_experimental_option('detach', True)
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_experimental_option('excludeSwitches', ['enable-automation'])

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)


# link_lst 에 각 페이지에 담긴 책의 링크를 얻는 함수
def get_links(lst):
    for i in range(1,4) :
        url = f"https://www.yes24.com/Product/Category/BestSeller?categoryNumber=001&pageNumber={i}"
        driver.get(url)
        
        datas = driver.find_elements(By.CLASS_NAME, 'gd_name')

        for j in  datas:
            lst.append(j.get_attribute('href'))
        time.sleep(1)

# 크롤링 데이터에서 숫자로만 데이터를 추출하는 함수
def get_num(arg) :
    temp = ""
    for i in arg : 
        if i.isdigit() :
            temp += i
    if temp == "" :
         temp = "0"
    return temp
     
# get_link()함수를 통해 얻은 링크에서 데이터를 크롤링하는 함수
def get_data(link):
        url = link
        driver.get(url)

        title = driver.find_element(By.CSS_SELECTOR, '.gd_name').text
        author = driver.find_element(By.CSS_SELECTOR, '.gd_auth a').text
        publisher = driver.find_element(By.CSS_SELECTOR, '.gd_pub a').text
        publishing_text = driver.find_element(By.CSS_SELECTOR, '.gd_date').text
        publishing = get_num(publishing_text)
        # 리뷰, 평점이 없는 경우는 0으로 처리.
        try :
            rating = driver.find_element(By.CSS_SELECTOR, '.gd_rating > .yes_b').text
        except NoSuchElementException :
            rating = "0"
        review_text = driver.find_element(By.CSS_SELECTOR, '.gd_reviewCount').text
        review = get_num(review_text)
        sales_text = driver.find_element(By.CSS_SELECTOR, '.gd_sellNum')
        sales = get_num(sales_text.text)
        price_text = driver.find_element(By.CSS_SELECTOR, '.nor_price > .yes_m')
        price = get_num(price_text.text)
        ranking_text = driver.find_element(By.CSS_SELECTOR, '.gd_best a')
        ranking = get_num(ranking_text.text)
        ranking_weeks_text = driver.find_element(By.CSS_SELECTOR, '.gd_best')
        ranking_weeks = get_num(ranking_weeks_text.text[-3:])
        
        # print(f"""
        #     책 제목 : {title}
        #     저자 : {author}
        #     출판사 : {publisher}
        #     출판일 : {publishing}
        #     평점 : {rating}점
        #     리뷰 : {review}건
        #     판매지수 : {sales}
        #     가격 : {price}원
        #     국내 도서 랭킹 : {ranking}위
        #     국내 도서 top100 : 연속 {ranking_weeks}주
        #     """)
        # time.sleep(1)

        # 데이터를 딕셔너리에 정리해서 반환
        data = {
            "title" : title,
            "author" : author,
            "publisher" : publisher,
            "publishing" : f"{publishing[:4]}-{publishing[4:6]}-{publishing[6:]}",
            "rating" : rating,
            "review" : review,
            "sales" : sales,
            "price" : price,
            "ranking" : ranking,
            "ranking_weeks" : ranking_weeks
        }

        return data

def execute_query(connection, query, args=None):
    with connection.cursor() as cursor:
        cursor.execute(query, args or ())
        if query.strip().upper().startswith('SELECT'):
            return cursor.fetchall()
        else:
            connection.commit()

def insert_data(connection,data):
    sql = """
    INSERT INTO Books (title, author, publisher, publishing, rating, review, sales, price, ranking, ranking_weeks)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    execute_query(connection, sql, (data["title"], data["author"], data["publisher"], data["publishing"], data["rating"], data["review"], data["sales"], data["price"], data["ranking"], data["ranking_weeks"]))
    print("데이터 추가 성공")

def main() : 
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='eodyd456@',
                                 db='yes24Crawl',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    
    link_lst = []
    get_links(link_lst)

    for i in link_lst:
        data = get_data(i)
        insert_data(connection, data)


if __name__ == "__main__":
    main()
        
# get_data('https://www.yes24.com/Product/Goods/124472862')