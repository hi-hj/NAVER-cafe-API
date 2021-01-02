# 동아리 홈페이지 이사

XpressEngine 기반 홈페이지를 네이버 카페로 이전했습니다.

웹 크롤러를 개발하여 기존 게시물을 저장했고, 네이버 카페 API를 활용하여 게시글을 작성했습니다.
<div>
<img src="https://img.shields.io/badge/BeautifulSoup-4.9.0-orange?style=flat-square" />
<img src="https://img.shields.io/badge/selenium-webdriver-orange?style=flat-square" />
</div>
<div>
<img src="https://img.shields.io/badge/SQlite-3.21.0-blue?style=flat-square" />
<img src="https://img.shields.io/badge/Django-3.1.4-blue?style=flat-square" />
</div>
<div>
<img src="https://img.shields.io/badge/NAVER-cafe-brightgreen?style=flat-square" />
<img src="https://img.shields.io/badge/NAVER-login-brightgreen?style=flat-square" />
</div>

- - -

### 웹 크롤링 : [web_crawler.py](https://github.com/HYUcoolguy/NAVER-cafe-API/blob/main/web_crawler.py)
03년부터 20년까지 축적된 게시물(게시글/댓글)을 추출
> BeautifoulSoup, Selenium 활용 <br>
> SQlite3에 데이터를 저장

1. DB 연결 & 세팅
2. ChromeDriver 실행
3. 로그인
4. for문으로 게시글 / 댓글 크롤링

- - -
### 네이버 카페 API

#### 1. [네이버 개발자 센터](https://developers.naver.com)

'애플리케이션 등록'

> 사용 API : 카페 <br>
> 서비스 환경 : PC 웹 (로컬에서만 실행) <br>
> 서비스 URL : http://127.0.0.1:8000/ <br>
> Callback URL : http://127.0.0.1:8000/

*관리자 계정 외에 API 사용 시, **멤버관리**에서 ID 추가*

- - -

#### 2. access token 발급 : [get_token.py](https://github.com/HYUcoolguy/NAVER-cafe-API/blob/main/get_token.py) 

1. 웹에서 사용할 계정으로 로그인
2. 파일 실행
3. console 창의 URL 클릭하여, code 값 확인

~~~json
code = "" // 여기에 추가!
access_token = "" //여기는 계속 비웁니다.
~~~

4. 파일 내 code에 해당 값 추가 <br>
5. 다시 파일 실행 <br>
6. cosnole 창에서 **access_token** 값 확인

- - -

#### 3. 네이버 카페 글쓰기 : [naver_write.py](https://github.com/HYUcoolguy/FAFA/blob/main/Back-End/FAFA/models.py) 

1. get_token.py 에서 얻은 access_token 값 입력 <br>
*token 유효 시간이 1시간이므로 주의* <br>
2. subject, content에 입력하고자 하는 값 추가
3. 파일 실행

*한글 깨짐 현상 : 개발자 센터 코드대로 하면 한글 깨짐 현상이 있다. 아래처럼 코드를 변경하면 정상적으로 인코딩 된다.*

*403 error : 첫 번째 함수는 정상 작동되지만, 두 번째 함수에서 403 error가 발생하는 경우. 함수 호출에 딜레이를 주면 해결할 수 있다. (403 error는 그 외에도 원인이 많음)*

*제목, 본문에 " 가 있으면 에러가 발생하는 현상 있음.  text.replace('\"', '\'') 사용하여 해결*
