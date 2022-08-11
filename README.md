# 나만의 알리미

- 계획 이유
```
"1. 외출하기 전 날씨 확인"
"2. 뉴스, 해외축구 확인"
"3. 축구, 야구 경기 일정 확인"
"위처럼 하루 일과 중 반복되는 일의 시간을 조금 줄일 수 없을까?" 고민하다가 크롤링 배운 것을 활용하여 나만의 알리미를 만들었습니다.
```

- 프로젝트 설계
```
def create_soup(url) :
    res = requests.get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    return soup
```
request 모듈을 활용하여 지정한 url에 HTTP GET 방식의 요청을 보내고,    
raiser_for_status()를 사용하여, 문제가 없으면 올바르게 내용을 가져오고, 문제가 있을 시 내용을 가져오지 않습니다.   
BeautifulSoup을 사용하여 첫 인자는 '특정 url에서 문제가 없어 올바르게 가져온 내용의 text'를, 두번째 인자는 'lxml parser'를 이용할지 명시했습니다.   
이 내용들이 한 사이트를 크롤링할 때 반복되므로, 함수로 지정하였으며, url은 함수의 매개변수로 입력받게 구성하였습니다.     

```
def weather() :
    url = "https://search.naver.com/search.naver?where=nexearch&sm=top_sug.asiw&fbm=1&acr=1&acq=%EC%84%9C%EC%9A%B8&qdt=0&ie=utf8&acir=1&query=%EC%84%9C%EC%9A%B8+%EB%82%A0%EC%94%A8"
    soup = create_soup(url)
    
    
    # 어제보다 OO' 높아요, 맑음
    cast = soup.find("p", attrs={"class" : "summary"}).get_text()
    cast = cast.replace("  "," ")

    # 현재 온도, OO'C
    temps = soup.find("div", attrs={"class" : "temperature_text"}).get_text()

    # 최고 / 최저 온도
    temps_rate = soup.find("span", attrs={"class" : "temperature_inner"}).get_text().strip()

    # 강수량
    cell_weather = soup.find("div", attrs={"class" : "cell_weather"}).get_text().strip()
    cell_weather = cell_weather.replace("   ","/")

    # 미세먼지
    air = soup.find("li", attrs={"class" : "item_today level2"}).get_text().strip()
    bot.send_message(id, text=
                    "[오늘의 날씨 알려드립니다.] \n"  +
                    (f"{temps[1:6]} : {temps[7:]}") +
                    (f"[{temps_rate}] \n") +
                    (f"  :  {cast} \n") +
                    (f"  :  {air} \n") +
                    ("[강수량 정보] \n") +
                    (f"{cell_weather}")
    )
```
날씨 정보를 가져오는 함수입니다.
네이버 날씨의 url을 weather함수의 지역변수 url로 지정하였으며, 위에서 만든 create_soup의 인자로 url을 등록해줍니다.  
가져올 데이터를 find 함수를 
