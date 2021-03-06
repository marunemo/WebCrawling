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
    태그의 속성의 추가, 조회, 삭제, 검색
    (attrs, get, dict 방식의 추가, 조회, 삭제, has_attr)
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
    
    print(parsedHtml.input.has_attr("test"))
    # -> True
    print(parsedHtml.input.has_attr("type"))
    # -> False

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
    print(parsedHtml.find_all(lambda tag : tag.has_attr("value") and not tag.has_attr('test')))
    # -> value 속성을 가지고 있으며, test 속성을 가지고 있지 않은 태그들 출력
    print(parsedHtml.find_all(lambda tag : tag.name == "input" and tag.has_attr("value") and not tag.has_attr('test')))
    # -> value 속성을 가지고 있으며, test 속성을 가지고 있지 않은 input 태그들 출력
    print(parsedHtml.find_all(lambda tag : tag.name == "input" and tag.has_attr("value") and not tag.has_attr('test') and "type" in tag.attrs and tag["type"] == "hidden"))
    # -> value 속성을 가지고 있으며, test 속성을 가지고 있지 않은 hidden 타입의 input 태그들 출력
    print(parsedHtml.find_all(id="gbv"))
    # -> id가 gbv인 태그들 출력
    print(parsedHtml.find_all(type="hidden"))
    # -> type이 hidden인 태그들 출력
    print(parsedHtml.find_all(id="gbv", type="hidden"))
    # -> id가 gbv이고, type이 hidden인 태그들 출력
    print(parsedHtml.find_all("input", id="gbv", type="hidden"))
    # -> id가 gbv이고, type이 hidden인 input 태그들 출력
    print(parsedHtml.find_all("input", attrs={"id" : "gbv", "type": "hidden"}))
    # -> id가 gbv이고, type이 hidden인 input 태그들 출력
    
    print(parsedHtml.find_all(name="gbv"))
    # -> []
    print(parsedHtml.find_all(attrs={"name" : "gbv"}))
    # -> [<input id="gbv" name="gbv" type="hidden" value="1"/>]
    # ==> 태그의 이름을 가리키는 name 키워드와 중첩되므로, name 속성을 찾기 위해서는 attrs에 딕셔너리 객체를 넣어 찾는 방법 밖에 없음
    
    print(parsedHtml.find_all(class_="gb1"))
    # -> class 속성에 gb1을 포함하는 태그들 출력
    print(parsedHtml.find_all(attrs={"class" : "gb1"}))
    # -> class 속성에 gb1을 포함하는 태그들 출력
    # ==> 파이썬 내에 class라는 키워드가 존재하므로, class 속성을 찾기 위해서는 class_라는 별칭이나 딕셔너리 객체를 사용해야 함
    print(parsedHtml.find_all(class_="lst"))
    # -> class 속성에 lst을 포함하는 태그들 출력 ([<input autocomplete="off" class="lst tiah" maxlength="2048" ... />])
    print(parsedHtml.find_all(class_="tiah"))
    # -> class 속성에 tiah을 포함하는 태그들 출력 ([<input autocomplete="off" class="lst tiah" maxlength="2048" ... />])
    print(parsedHtml.find_all(class_="lst tiah"))
    # -> class 속성에 lst tiah을 포함하는 태그들 출력 ([<input autocomplete="off" class="lst tiah" maxlength="2048" ... />])
    print(parsedHtml.find_all(class_="tiah lst"))
    # -> class 속성에 tiah lst을 포함하는 태그들 출력 ([])
    print(parsedHtml.select(".tiah.lst"))
    # -> class 속성에 tiah와 lst를 모두 포함하는 태그들 출력 ([<input autocomplete="off" class="lst tiah" maxlength="2048" ... />])
    print(parsedHtml.select("html > head > meta"))
    # -> html 태그 안의 head 태그 안에 있는 모든 meta 태그들 출력

    # html의 형태로 저장(prettify로 자동 정렬 및 레이아웃)
    f = open("result.html", "w", encoding="utf-8")
    f.write(parsedHtml.prettify())
    f.close()
else:
    print(res.status_code) 