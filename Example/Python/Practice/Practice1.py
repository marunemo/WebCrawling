import requests
from bs4 import BeautifulSoup as bs
from bs4.element import NavigableString, Tag

# 열의 데이터 중 문자열만 추출하여 작성
# </td>(td closing tag)가 없을 경우에 td 태그에 상속되어 있는 tr이나 td를 재귀적으로 처리
def tableDataParser(td, csvFile):
    # 각 셀을 큰따옴표로 구분짓기 위한 문자열
    # 구분 문자인 ","이 테이블 내에서도 텍스트의 형태로 나타날 시에 csv 파일에서 두 문자를 구분하도로 하기 위함
    parsedText = ""

    # 병합된 셀과 다른 셀의 열을 맞추기 위함
    if td.has_attr("colspan") and int(td["colspan"]) > 1:
        colspan = int(td["colspan"])
    else:
        colspan = 1

    # td 안의 텍스트와 태그를 모두 추출
    for data in td.descendants:
        if type(data) == NavigableString:
            # td 내부의 텍스트는 상속된 태그에 관계없이 하나의 텍스트로 간주
            parsedText += data.strip()
        elif type(data) == Tag:
            if data.name == "br":
                # 만약 </br>이라면 줄내림 대신 띄어쓰기로 처리
                parsedText += " "
            elif data.name == "td":
                # td 태그에 상속되어 있는 td 태그의 경우,
                # tr과 달리 상속된 태그의 텍스트로서 추출이 가능하나 서로 다른 td끼리 분리시켜야 하므로 구분 문자만 입력
                
                # 현재 병합된 열 개수만큼 공백 추가
                for _ in range(colspan - 1):
                    parsedText += "\", \"" 
                
                parsedText = parsedText.strip() + "\", \""

                # 만약 이번 td도 병합되어 있다면 그 개수 추가
                if td.has_attr("colspan") and int(td["colspan"]) > 1:
                    colspan = int(td["colspan"])
                else:
                    colspan = 1
            elif data.name == "tr":
                # 만약 td 태그 내에 tr이 상속되어 있다면 해당 태그를 tr 태그로서 처리
                # 또한, tr 태그가 나왔다는 것은 td 태그가 끝났다는 의미이므로, 즉시 td 내부 탐색을 종료

                # 현재 병합된 열 개수만큼 공백 추가
                for _ in range(colspan - 1):
                    parsedText += "\", \""

                csvFile.write("\"" + parsedText.strip() + "\", \n")
                tableRowParser(data, csvFile)
                return
    
    # 현재 병합된 열 개수만큼 공백 추가
    for _ in range(colspan - 1):
        parsedText += "\", \""

    # 문자열을 "로 감싸서 작성
    csvFile.write("\"" + parsedText.strip() + "\", ")


# 행에서 td 태그만 추려내어 데이터 탐색
def tableRowParser(tr, csvFile):
    for col in tr.children:
        if type(col) == Tag and col.name == "td":
            tableDataParser(col, csvFile)

# 추출한 html 파일의 </td> 태그(closing tag) 누락 문제로 함수의 형태로 사용
# tableRowParsing과 tableDataParsing을 이용한 재귀적인 처리를 위함
def tableToCSV(table, csvFile):
    for row in table.children:
        if type(row) == Tag and row.name == "tr":
            tableRowParser(row, csvFile)
            csvFile.write('\n')

# robots.txt 파일을 map 형식으로 변환
def robotsTxtParser(targetURL: str):
    if not targetURL.startswith("http"):
        targetURL = "http://" + targetURL

    robotsTxt = requests.get(targetURL + "/robots.txt")
    if robotsTxt.status_code != 200:
        raise Exception("HTTP 상태 코드: " + str(robotsTxt.status_code))

    robotsProtocol = {"User-agent" : [], "Allow" : [], "Disallow" : []}
    for line in robotsTxt.text.replace("\r", "").split("\n"):
        key, value = line.split(": ")
        if key in robotsProtocol:
            robotsProtocol[key].extend(value.split())
        else:
            robotsProtocol[key] = [value]
    
    return robotsProtocol

# 특정 단어가 포함된 표를 csv 파일의 형식으로 출력
def tableExtractor(seed: list, includeString: str, robotsProtocol: list = [], fileNames: list = []):

    if fileNames != [] and len(seed) != len(fileNames):
        raise Exception("URL의 개수와 저장 파일의 개수가 다릅니다.")

    # 주어진 URL들로부터 html 데이터 탐색
    for index, url in enumerate(seed):
        if not url.startswith("http"):
            url = "http://" + url

        if "*" in robotsProtocol["User-agent"]:
            for disallowPath in robotsProtocol["Disallow"]:
                if targetURL + disallowPath in url:
                    raise Exception(url + "은 " + disallowPath + "에 의하여 접근이 제한되어있습니다.")
        else:
            raise Exception("User-agnet에 의하여 접근이 제한되어있습니다.")
        
        # 결과 출력 파일
        if fileNames == []:
            fileName = url[url.index("/", len("https://") + 1) + 1:]
            resultCSV = open(fileName + ".csv", "w", encoding="utf-8")
        else:
            resultCSV = open(fileNames[index] + ".csv", "w", encoding="utf-8")

        # 만약 접근 가능한 URL이라면 get 방식 접근
        res = requests.get(url, timeout=1)

        # 접속 결과 출력
        if res.status_code != 200:
            print("접속 실패 : " + url)
        else:
            # 접속 성공 시 접속 성공 문구와 함께 html 구문 분석 실행
            print("접속 성공 : " + url)
            
            # beautiful soup 객체 변환
            html = bs(res.text, "html.parser")

            # 만조시각 텍스트를 가진 태그 탐색
            targetTable = html.find_all(lambda tag : tag.string and includeString in tag.string)[0]

            # 해당 태그를 가지고 있는 table 태그 추적
            while targetTable.name != "table":
                targetTable = targetTable.parent

            # table 태그의 각 열과 행의 데이터 수집
            tableToCSV(targetTable, resultCSV)
        
        resultCSV.close()

if __name__ == "__main__":
    # 대상 URL
    targetURL = "www.badatime.com"

    # robots.txt 파일로부터 규칙 다운로드
    robotsProtocol = robotsTxtParser(targetURL)

    # 탐색할 URL 시드 입력
    seed = []
    seed.append("https://www.badatime.com/127-2021-09-01.html")
    seed.append("www.badatime.com/127-2021-10-01.html")
    seed.append("http://www.badatime.com/127-2021-11-01.html")

    # 수동 파일명 지정
    fileNames = []
    fileNames.append("2021년 9월")
    fileNames.append("2021년 10월")
    fileNames.append("2021년 11월")

    # 테이블 추출
    tableExtractor(seed, "만조시각", robotsProtocol, fileNames)