import requests
from bs4 import BeautifulSoup as bs

# 대상 URL
targetURL = "https://www.badatime.com"

# robots.txt 확인
robotsTxt = requests.get(targetURL + "/robots.txt")

# 접근할 수 없을 시 오류 출력
if robotsTxt.status_code != 200:
    raise Exception("HTTP 상태 코드: " + str(robotsTxt.status_code))

# 결과 출력 파일
resultCSV = open("result.csv", "w", encoding="utf-8")

# 크롤링할 수 있는 지 탐색
searchAble = {"User-agent" : [], "Allow" : [], "Disallow" : []}
for line in robotsTxt.text.replace("\r", "").split("\n"):
    key, value = line.split(": ")
    if key in searchAble:
        searchAble[key].extend(value.split())
    else:
        searchAble[key] = [value]

# 탐색할 URL 시드 입력
seed = []
seed.append("https://www.badatime.com/127-2022-09-01.html")

# 주어진 URL들로부터 html 데이터 탐색
for url in seed:
    if "*" in searchAble["User-agent"]:
        for disallowPath in searchAble["Disallow"]:
            if targetURL + disallowPath in url:
                raise Exception(url + "은 " + disallowPath + "에 의하여 접근이 제한되어있습니다.")
    
    # 만약 접근 가능한 URL이라면 get 방식 접근
    res = requests.get(url, timeout=1)

    # 접속 결과 출력
    if res.status_code == 200:
        print("접속 성공 : " + url)
    else:
        print("접속 실패 : " + url)
    
    # beautiful soup 객체 변환
    html = bs(res.text, "html.parser")

    # 만조시각 텍스트를 가진 태그 탐색
    targetTable = html.find_all(lambda tag : tag.string and "만조시각" in tag.string)[0]

    # 해당 태그를 가지고 있는 table 태그 추적
    while targetTable.name != "table":
        targetTable = targetTable.parent

    # table 태그의 각 열과 행의 데이터 수집
    for row in targetTable.children:
        if row.name == "tr":
            for data in row.children:
                resultCSV.write("\"")
                if data.string != None:
                    resultCSV.write(data.string.strip())
                else:
                    for text in data.children:
                        if text.string != None:
                            resultCSV.write(text.string.strip())
                        elif text.name == "br":
                            resultCSV.write(" ")
                resultCSV.write("\",")
            resultCSV.write("\n")

resultCSV.close()