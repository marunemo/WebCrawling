import requests
from bs4 import BeautifulSoup as bs
from bs4.element import NavigableString, Tag

# 열의 데이터 중 문자열만 추출하여 작성
# </td>(td closing tag)가 없을 경우에 td 태그에 상속되어 있는 tr이나 td를 재귀적으로 처리
def tableDataParsing(td, csvFile):
    # td 안의 텍스트와 태그를 모두 추출
    for data in td.descendants:
        if type(data) == NavigableString:
            # td 내부의 텍스트는 상속된 태그에 관계없이 하나의 텍스트로 간주
            csvFile.write(data.strip())
        elif type(data) == Tag:
            if data.name == "br":
                # 만약 </br>이라면 줄내림 대신 띄어쓰기로 처리
                csvFile.write(" ")
            elif data.name == "td":
                # td 태그에 상속되어 있는 td 태그의 경우,
                # tr과 달리 상속된 태그의 텍스트로서 추출이 가능하나 서로 다른 td끼리 분리시켜야 하므로 ", "만 입력
                csvFile.write(", ")
            elif data.name == "tr":
                # 만약 td 태그 내에 tr이 상속되어 있다면 해당 태그를 tr 태그로서 처리
                # 또한, tr 태그가 나왔다는 것은 td 태그가 끝났다는 의미이므로, 즉시 td 내부 탐색을 종료
                csvFile.write("\n")
                tableRowParsing(data, csvFile)
                break

# 행에서 td 태그만 추려내어 데이터 탐색
def tableRowParsing(tr, csvFile):
    for col in tr.children:
        if type(col) == Tag and col.name == "td":
            tableDataParsing(col, csvFile)
            csvFile.write(", ")

# 추출한 html 파일의 </td> 태그(closing tag) 누락 문제로 함수의 형태로 사용
# tableRowParsing과 tableDataParsing을 이용한 재귀적인 처리를 위함
def tableToCSV(table, csvFile):
    for row in table.children:
        if type(row) == Tag and row.name == "tr":
            tableRowParsing(row, csvFile)
            csvFile.write('\n')

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
    # html = bs(res.text, "html.parser")
    html = bs(res.text, "html.parser")

    # 만조시각 텍스트를 가진 태그 탐색
    targetTable = html.find_all(lambda tag : tag.string and "만조시각" in tag.string)[0]

    # 해당 태그를 가지고 있는 table 태그 추적
    while targetTable.name != "table":
        targetTable = targetTable.parent

    # table 태그의 각 열과 행의 데이터 수집
    tableToCSV(targetTable, resultCSV)

resultCSV.close()