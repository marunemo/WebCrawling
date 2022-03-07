# [ref] https://beautiful-soup-4.readthedocs.io/en/latest/

import requests
from bs4 import BeautifulSoup

# 구글 시작 페이지를 get 방식으로 가져옴
res = requests.get("https://www.google.co.kr", timeout=1)

# 만약 요청에 대한 응답이 성공했다면, BeautifulSoup 객체로 변경
if res.status_code == 200:
    html = res.text
    parsedHtml = BeautifulSoup(html, 'html.parser')
    print(type(parsedHtml))
    
    f = open("result.html", "w", encoding="utf-8")
    f.write(parsedHtml.prettify())
    f.close()
else:
    print(res.status_code) 