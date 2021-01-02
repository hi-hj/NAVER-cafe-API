from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time, re
import pandas as pd
import requests
import sqlite3
from urllib.parse import urlparse


# 1. DB 연결 / 세팅
## DB : sqlite3
DB = 'YB_BOARD.db'
BOARD_NAME = 'YB_BOARD_TEST'
conn = sqlite3.connect(DB)
cur = conn.cursor()
# 본문들을 저장할 테이블 
sql = 'CREATE TABLE IF NOT EXISTS '+ BOARD_NAME+' ("count" INTEGER, "title" TEXT, "time" TEXT, "writer" TEXT, "content" TEXT);'
cur.execute(sql) 
conn.commit()
# 댓글들을 저장할 테이블 (_com 텍스트 추가)
sql = 'CREATE TABLE IF NOT EXISTS '+BOARD_NAME+'_com ("count" INTEGER, "com_writer" TEXT, "com_time" TEXT, "com_content" TEXT);'
cur.execute(sql) 
conn.commit()

conn.close()


# 2. ChomreDriver 불러오기
path = 'C:/Users/hyeon/OneDrive/바탕 화면/club_web_crawl/chromedriver.exe' # 윈도우 
driver = webdriver.Chrome(path)
driver.get("http://hyuscuba.com")
assert "한양대학교 스킨스쿠버 다이빙클럽" in driver.title


# 3. 원하는 사이트에 로그인 (로그인이 필요한 경우에만)
# 1차 로그인
usr = '##########'
pwd = '##########'
elem = driver.find_element_by_id("fo_login_widget")
elem.click()
elem = driver.find_element_by_id("user_id")
elem.send_keys(usr)
elem = driver.find_element_by_id("user_pw")
elem.send_keys(pwd)
elem.send_keys(Keys.RETURN)
# 2차 로그인 (확인 버튼)
elem = driver.find_element_by_css_selector('div.login-body > p > a')
elem.click()
# 3차 로그인 
elem = driver.find_element_by_id("uid")
elem.send_keys(usr)
elem = driver.find_element_by_id("upw")
elem.send_keys(pwd)
elem.send_keys(Keys.RETURN)
# 4차 로그인
driver.refresh()
driver.get('http://hyuscuba.com/xe/ybboard')



# 4. 데이터 크롤링 시작
# YB 게시판
driver.get('http://hyuscuba.com/xe/ybboard')

for i in range(88, 130): #PAGE COUNT :130
    driver.get('http://hyuscuba.com/xe/index.php?mid=ybboard&page='+str(i+1))
    for j in range(20): #BOARD COUNT : 20
        # 4-1. URL 패턴 / HTML, CSS (ID/CLASS) 패턴 분석하여 원하는 페이지 찾는 로직짜기
        #게시글 클릭
        elem = driver.find_element_by_css_selector('#board_list > table > tbody > tr:nth-child('+str(j+1)+') > td.title > a:nth-child(1)')
        elem.click()


        #   크롤링 실시
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        #게시글 / 댓글 COUNT
        count   = i*20 + j
        #       게시글 내용
        title   = soup.select_one('div.read_header > h1').text
        date    = soup.select_one('body > div.user_layout > div.body > div > div > div.board_read > div.read_header > p.time').string[0:14]
        writer  = soup.select_one('body > div.user_layout > div.body > div > div > div.board_read > div.read_header > p.meta').text
        content = soup.select_one('div.read_body').text
        com_num = soup.select_one('div#comment > div.fbHeader > h2 > em').string
        
    # 5. 크롤링한 데이터를 저장 (이 코드에서는 dbsqlite3 사용)
        #DB에 저장 : 본문
        conn = sqlite3.connect(DB)
        cur = conn.cursor()
        sql = "replace into %s(count,title,time,writer,content) values (?,?,?,?,?)" %BOARD_NAME
        cur.execute(sql, (count,title,date,writer,content))
        conn.commit()
        
    
    # 6. 댓글은 '동일한 db 파일'의 '다른 BOARD'에 저장
        #       댓글 내용
        for k in range(int(com_num)):
            com_writer  = soup.select_one('div#comment  li.fbItem:nth-child('+str(k+1)+') .fbMeta .author').string
            com_time    = soup.select_one('div#comment  li.fbItem:nth-child('+str(k+1)+') p.time').string[0:10]
            com_content = soup.select_one('div#comment  li.fbItem:nth-child('+str(k+1)+') div:nth-child(2)').text

            
            sql = "replace into '%s_com'(count,com_writer,com_time,com_content) values (?,?,?,?)" %BOARD_NAME
            cur.execute(sql, (int(count),str(com_writer),str(com_time),str(com_content)))
            conn.commit()

        conn.close()
        

        
