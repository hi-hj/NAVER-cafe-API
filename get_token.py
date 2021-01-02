# coding=utf-8
import requests
import base64

#리다이렉트 주소입력
redirect_uri= "http://127.0.0.1:8000/"

# 오픈API 등록후 발급
client_id ="*****" # Your Client_ID
client_secret = "*****"
state = "REWERWERTATE" # 아무 텍스트 와도 상관 없음


# 1차로 코드 발급해야합니다.
code = ""
# 2차로 발급받은 코드로 액세스 코드를 발급받아야 합니다.
access_token = ""

# code get
if not code:
    url = f'https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&state={state}'
    print(url)

#access token 발급
if not access_token:
    #login_token
    # base64 encode get
    clientConnect = client_id + ":" + client_secret
    clidst_base64 = base64.b64encode(bytes(clientConnect, "utf8")).decode()

    url = f'https://nid.naver.com/oauth2.0/token?grant_type=authorization_code&client_id={client_id}&client_secret={client_secret}&redirect_uri={redirect_uri}&code={code}&state={state}'
    r = requests.get(url,headers={"Authorization": "Basic "+clidst_base64})
    print(r.text)