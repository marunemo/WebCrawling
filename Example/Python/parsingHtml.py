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
    (name, string, parent(going up), children, contents, descendants(going down))
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
    print("=" * 20)
    for child in parsedHtml.head.children:
        print(child.name)
    print("=" * 20)
    # -> ㄱ
    # meta
    # meta
    # title
    # script
    # style
    # style
    # script
    print(parsedHtml.title)
    # -> <title>Google</title>
    print(type(parsedHtml.head.children), len(list(parsedHtml.head.children)))
    # -> <class 'list_iterator'> 7 (태그만을 children으로 간주)
    print(type(parsedHtml.head.contents), len(parsedHtml.head.contents))
    # -> 7 (태그만을 children으로 간주)
    print(len(list(parsedHtml.head.descendants)))
    # -> 12 (스트링까지 children으로 간주)
    
    print(type(parsedHtml.div))
    # -> <class 'bs4.element.Tag'>
    print(parsedHtml.div)
    # -> 맨 처음 나타나는 div 태그
    print(parsedHtml.body.div.div)
    # -> body에서 맨 처음 나타나는 div 태그 안의 맨 처음 나타나는 div 태그

    '''
    태그의 iterator
    '''
    print(parsedHtml.head.contents[0].name)
    # -> meta
    print("===== next sibling ===== :", parsedHtml.head.contents[0].name)
    for sibling in parsedHtml.head.contents[0].next_siblings:
        print(sibling.name)
    # -> ㄱ
    # meta
    # title
    # script
    # style
    # style
    # script
    print("===== previous sibling ===== :", parsedHtml.head.contents[-1].name)
    for sibling in parsedHtml.head.contents[-1].previous_siblings:
        print(sibling.name)
    # -> ㄱ
    # style
    # style
    # script
    # title
    # meta
    # meta

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
    
    '''
    태그 내 문자열의 조회 및 변경
    '''
    print(parsedHtml.title)
    # -> <title>Google</title>
    print(parsedHtml.title.string)
    # -> Google
    parsedHtml.title.string = "구글1"
    print(parsedHtml.title)
    # -> <title>구글1</title>
    parsedHtml.title.string.replace_with("구글2")
    print(parsedHtml.title)
    # -> <title>구글2</title>

    '''
    태그 탐색
    '''
    print(type(parsedHtml.find_all("input")))
    # -> <class 'bs4.element.ResultSet'>
    print(parsedHtml.find_all("input"))
    # -> 상위 태그에 상속되어 있는 모든 input 태그들을 ResultSet의 형태로 출력
    print(parsedHtml.find_all(["title", "input"]))
    # -> 상위 태그에 상속되어 있는 모든 title 태그와 input 태그들을 ResultSet의 형태로 출력

    # f = open("result.html", "w", encoding="utf-8")
    # f.write(parsedHtml.prettify())
    # f.close()
else:
    print(res.status_code) 