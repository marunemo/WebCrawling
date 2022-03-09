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

    '''
    태그의 접근과 태그의 프로퍼티
    (name, string, parent)
    '''
    print(parsedHtml.title)
    # -> <title>Google</title>
    print(parsedHtml.title.name)
    # -> title
    print(parsedHtml.title.string)
    # -> Google
    print(parsedHtml.title.parent)
    # -> head 태그의 모든 것
    print(parsedHtml.title.parent.name)
    # -> head
    print(parsedHtml.title.parent.string)
    # -> None
    
    print(type(parsedHtml.div))
    # -> <class 'bs4.element.Tag'>
    print(parsedHtml.div)
    # -> 현재 최상위에 속해 있는 div 태그들이 띄어쓰기나 줄 바꿈 없이 전부 출력

    '''
    태그의 속성의 추가, 조회, 삭제
    (attrs, get, dict 방식의 추가, 조회, 삭제)
    '''
    print(parsedHtml.input)
    # -> <input name="ie" type="hidden" value="EUC-KR"/>
    print(parsedHtml.input.attrs)
    # -> {'name': 'ie', 'value': 'EUC-KR', 'type': 'hidden'}
    print(parsedHtml.input["name"])
    # -> ie
    print(parsedHtml.input["type"])
    # -> hidden
    print(parsedHtml.input["value"])
    # -> EUC-KR
    print(parsedHtml.input.get("value"))
    # -> EUC-KR

    parsedHtml.input["test"] = "temp"
    # input 태그에 새로운 속성 추가
    print(parsedHtml.input)
    # -> <input name="ie" test="temp" type="hidden" value="EUC-KR"/>
    print(parsedHtml.input.attrs)
    # -> {'name': 'ie', 'value': 'EUC-KR', 'type': 'hidden', 'test': 'temp'}
    parsedHtml.input["test"] = ["temp", "my temp"]
    # input 태그에 새로운 속성 복수 추가
    print(parsedHtml.input)
    # -> <input name="ie" test="temp my temp" type="hidden" value="EUC-KR"/>
    print(parsedHtml.input.attrs)
    # -> {'name': 'ie', 'value': 'EUC-KR', 'type': 'hidden', 'test': ['temp', 'my temp']}
    print(type(parsedHtml.input.attrs))
    # -> <class 'dict'>
    print(type(parsedHtml.input.attrs["test"]))
    # -> <class 'list'>

    del parsedHtml.input["type"]
    # input 태그에 새로운 속성 삭제
    print(parsedHtml.input)
    # -> <input name="ie" test="temp" value="EUC-KR"/>
    print(parsedHtml.input.attrs)
    # -> {'name': 'ie', 'value': 'EUC-KR', 'test': 'temp'}
    
    print(type(parsedHtml.find_all("input")))
    # -> <class 'bs4.element.ResultSet'>
    print(parsedHtml.find_all("input"))
    # -> 상위 태그에 상속되어 있는 모든 input 태그들 ResultSet의 형태로 출력

    # f = open("result.html", "w", encoding="utf-8")
    # f.write(parsedHtml.prettify())
    # f.close()
else:
    print(res.status_code) 