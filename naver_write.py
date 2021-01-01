import os
import sys
import urllib.request
import sqlite3
from urllib.parse import urlencode
import time

# Get data from sqlite3
DB = 'YB_BOARD.db'
BOARD_NAME = 'YB_BOARD_TEST'
conn = sqlite3.connect(DB)
cur = conn.cursor()

token = "AAAAOqlO4rT5yZyRfS7wabDSJv30uARtgDjVHNXMPBu4TobuIKkTHhYENVPMJ7706iXQJNLrW_tC8CbkKtmQyEpXH3o"
header = "Bearer " + token # Bearer 다음에 공백 추가
clubid = "30067107" # 카페의 고유 ID값
menuid = "10" # (상품게시판은 입력 불가)
url = "https://openapi.naver.com/v1/cafe/" + clubid + "/menu/" + menuid + "/articles"

def naver_upload():
    global row
    global header
    global clubid
    global menuid
    global url
    print(row[0])
    subject = urllib.parse.quote('['+row[3].strip()[0:3]+'] ' + row[1])
    content = urllib.parse.quote(row[4].replace('\"', '\''))
    data = urlencode({'subject': subject, 'content': content}).encode()
    request = urllib.request.Request(url, data=data)
    request.add_header('Authorization',header)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        print(response_body.decode('utf-8'))
    else:
        print("Error Code:" + rescode)
for row in cur.execute("SELECT * FROM YB_BOARD_TEST ORDER BY 1 DESC LIMIT 200 OFFSET 1422"):
    # print(row[1])
    # print(row[3])
    # print(row[4].replace('\"', '\''))
    naver_upload()
    time.sleep(10)
