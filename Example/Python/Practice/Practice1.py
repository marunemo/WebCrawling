import requests
from bs4 import BeautifulSoup as bs

# 대상 URL
targetURL = "https://www.badatime.com"

# robots.txt 확인
robotsTxt = requests.get(targetURL + "/robots.txt")

# 접근할 수 없을 시 오류 출력
if robotsTxt.status_code != 200:
    raise Exception("HTTP 상태 코드: " + str(robotsTxt.status_code))

# 크롤링할 수 있는 지 탐색
searchAble = {"User-agent" : [], "Allow" : [], "Disallow" : []}
for line in robotsTxt.text.replace("\r", "").split("\n"):
    key, value = line.split(": ")
    if key in searchAble:
        searchAble[key].extend(value.split())
    else:
        searchAble[key] = [value]

seed = []
for url in seed:
    if "*" in searchAble["User-agent"] and url.replace(targetURL, "") in searchAble["Disallow"]:
        raise Exception(url + "에 접근이 제한되어있습니다.")