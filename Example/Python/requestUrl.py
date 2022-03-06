# [ref] https://docs.python-requests.org/en/latest/

import requests

tab = "/search"
getParams = {"q" : "감자", "rlz" : "1C1OKWM_koKR986KR986", "oq" : "감자", "aqs" : "chrome..69i57.1694j0j1", "sourceid" : "chrome", "ie" : "UTF-8"}
res = requests.get("https://www.google.co.kr" + tab, params=getParams, timeout=1)

# URL 확인
print(res.url)

# 200 = 서버가 요청을 제대로 처리했다는 뜻이다. 이는 주로 서버가 요청한 페이지를 제공했다는 의미로 쓰인다.
# [ref] https://ko.wikipedia.org/wiki/HTTP_%EC%83%81%ED%83%9C_%EC%BD%94%EB%93%9C
print(res.status_code)

# 결과 html 파일 출력
f = open("result.html", "w")
f.write(res.text)
f.close()