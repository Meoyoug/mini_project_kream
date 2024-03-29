# Mini-Project Kream-Crawling

## Introduce
This project was developed during the Oz-bootcamp program. As a mini project, I created an app for crawling a trading platform called KREAM.

It runs only in the local environment because server deployment has not been performed.

## Tech Stack
### Language
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)

### Back-end
![MySQL](https://img.shields.io/badge/mysql-%2300f.svg?style=for-the-badge&logo=mysql&logoColor=white)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![Jinja](https://img.shields.io/badge/jinja-white.svg?style=for-the-badge&logo=jinja&logoColor=black)

### Front-end
![Bootstrap](https://img.shields.io/badge/bootstrap-%238511FA.svg?style=for-the-badge&logo=bootstrap&logoColor=white)

### Crawling
![Selenium](https://img.shields.io/badge/-selenium-%43B02A?style=for-the-badge&logo=selenium&logoColor=white)

## How to Run
1. Download .zip file
2. install library
    ```terminal
    pip install requirements.txt
    ```
3. If MySQL is not installed, you need to install MySQL.
4. Once MySQL is installed, create a database in MySQL Workbench and execute the `kream_schema.sql` file.
5. setup is complete, you can run the `run.py` at the top level of the folder.
6. Access the local host on port 5000 using a web browser.


## UPDATE History

### 2024.01.04
- Bootstrap v5.3 사용
- JS updateDate함수를 통해 정시마다 시간업데이트 되도록 설정
- 카테고리, 성별을 드롭다운박스로 구현하여 선택후에 적용하여 검색조건을 설정.
- 로드된 상품목록에서 카테고리를 선택해 지울 수 있도록 설정

### 2024.01.09 update
- kream.py 를 이용해 크림 홈페이지에서 신상품을 크롤링한 데이터를 json형식으로 인코딩 후  crawled_data.json 파일로 저장
- js 에서 crawled_data.json 파일을 불러와서 디코딩 후에 data 배열에 담을 수 있도록 함

### 2024.01.17 update
- selenium을 이용하여 크롤링한 데이터를 pymysql을 이용해 MySQL db에 담을 수 있도록 만든 kream3.py 추가
- kream3.py에서 수정하여 pymysql을 제외시키고 pymongo를 이용하여 MongoDB에 데이터베이스를 만들도록 한 kream4.py 추가

### 2024.01.20 update
- crawling.py 개선
    1. 중복되는 항목에 대한 데이터 삽입을 금지
    2. 카테고리, 성별을 별도로 가져오도록 get_category 함수를 생성
    3. 제품의 한글 이름도 알 수 있도록 kr_description 변수를 통해 가져오도록 함

- 검색 기능추가
    1. index.html 에서 form을 이용하여 get방식으로 검색로직을 구현할 수 있도록 수정
    2. search_data.py 에서 입력받은 카테고리, 성별의 값을 각각 request.args.getlist로 받고 검색어를 request.args.get으로 받은 다음 알고리즘에 의한 검색결과를 sql문으로 서버에서 가져온 다음 render_template으로 검색결과 페이지에 대한 html문서를 가져오도록함.

- 삭제버튼 기능 구현
    1. adminPage.js에서 삭제버튼에대한 이벤트 리스너를 등록하고 post방식으로 /delete라우터로 전달함으로써 삭제방식을 구현함
    2. delete.py에서 request.get_json()을 통해 삭제할 행의 데이터를 받아온다음 sql문으로 해당되는 데이터를 지우는 방식으로 구현
    3. 이후에 응답으로 성공 실패여부를 이벤트리스너에 등록된 함수에서 판별하여 삭제된 데이터를 페이지에 반영하도록함

- 페이지네이션 기능 구현
    1. flask-paginate 기능을 이용함.
    2. 페이지당 노출되는 아이템의 개수와 offset, 페이지정보는 get_page_args() 함수를 이용하였으며 이를 바탕으로 Pagination 객체를 생성함
    3. 생성된 객체를 데이터와함께 render_template 함수를 통해 html에 전달하여 html에서 이를 이용해서 페이지네이션을 구현하도록함.

### 2024.01.24 update
- flask 앱 파일들을 구조화 하여 정리함.
    1. 각 기능에 대한 함수작성 후에 라우트를 지정하고 블루프린터를 지정함.
    2. __init__.py 에서 앱의 플라스크 객체를 생성하고 지정한 블루프린터들을 등록하도록함.
    3. run.py를 통해 앱을 실행시킬 수 있도록 구현함.
    4. 필요한 이미지 파일과 js,css 파일은 static 폴더안에서 불러올 수 있도록 하였음
    5. html은 templates 폴더 안에서 불러올 수 있도록 함.
    6. 블루프린터에 등록함에 따라 html에서 url_for로 경로 지정하는 방식을 모두 바꿔줌

- 상품 목록 업데이트 버튼을 만들어서 이벤트 리스너를 등록하였움. 클릭하면 크롤링 파일이 실행되고 페이지를 새로 로드하여서 업데이트하도록 구현함.

- 상품 정보에 '상품 상세 보기' 버튼 추가
    1. 크롤링 파일에서 해당 상품에 대한 링크를 가져오도록 하고 MySQL DB에 저장하도록함
    2. html에서 Jinja2 엔진 템플릿을 이용하여 반복문을 통해 각 상품 항목별로 버튼이 생기도록 함.
    3. 생성된 버튼은 form, get 형식으로 버튼을 누르면 해당 링크로 이동 하도록 구현함.

### 2024.01.24 update (2)
- 상단에 네비게이션 바 추가
    1. Bootstrap v5.3.1 에서 지원하는 navvar 클래스 이용.
    2. 네비게이션 바 기능
        - 홈 버튼
        - infomation 버튼 (추후 기능 구현 예정)
        - 카테고리 드롭다운 : 선택한 카테고리의 검색결과를 보여주는 페이지로 이동
        - 성별 드롭다운 : 선택한 성별의 검색결과를 보여주는 페이지로 이동
    3. 검색 결과를 보여주는 템플릿을 따로 두지않고 index.html을 이용하는 것으로 변경

### 2024.01.25 update
- 상단 네비게이션바의 information 항목을 클릭하면 미니프로젝트에 대한 정보가 담겨있는 페이지로 이동
- 이를 위해 info.html 생성하고 info.py를 생성하여 블루프린터로 등록

## 2024.01.26 update
- Referer Policy를 HTML head에 추가하여 이미지 깨짐 현상 해결, 상품정보를 Bootstrap의 카드를 이용하여 가시성을 높임.