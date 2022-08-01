import telegram
import requests
from bs4 import BeautifulSoup
import time

bot = telegram.Bot(token = "5433279502:AAF1snTj1bPTAjLwYj5BFfvgsZKDvN7tT84")
id = '@AlarmBotmadeEunbae'


def create_soup(url) :
    res = requests.get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    return soup

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
                    "[오늘의 날씨] \n"  +
                    (f"{temps[1:6]} : {temps[7:]}") +
                    (f"[{temps_rate}] \n") +
                    (f"  :  {cast} \n") +
                    (f"  :  {air} \n") +
                    ("[강수량 정보] \n") +
                    (f"{cell_weather}")
    )
    
def scrap_news() :
    url = "https://media.naver.com/press/001"
    soup = create_soup(url)

    main_news = soup.find("ul", attrs={"class" : "press_news_list as_bottom"}).find_all("li", limit=5)
    for index, news in enumerate(main_news) :
        title = news.find("a").get_text().strip()
        link = news.find("a")["href"]
        bot.send_message(id, text=
                            "[오늘의 뉴스] \n" +
                            (f"{index + 1}. {title} \n") +
                            (f"    (링크 : {link})")
        )

def sports_news() :
    url = "https://sports.news.naver.com/wfootball/index"
    world_football_url = "https://sports.news.naver.com/"
    soup = create_soup(url)
    
    sports = soup.find("ul", attrs={"class" : "home_news_list"}).find_all("li")
    for index, news in enumerate(sports) :
        title = news.find("a").get_text().strip()
        link = world_football_url + news.find("a")['href']
        bot.send_message(id, text =
                         "[오늘의 해외축구] \n" +
                         (f"{index+1}. {title}\n") +
                         (f"    (링크 : {link})")
        )

def baseball_match() :
    url = "https://sports.news.naver.com/kbaseball/index"
    soup = create_soup(url)


    kboMatch = soup.find_all("div", id="_tab_box_kbo")[0]
    kboMatchItems = kboMatch.find("div", class_="hmb_list").find_all("li", class_="hmb_list_items")
    bot.send_message(id, "[야구 경기 예정 및 결과]\n")
    for item in kboMatchItems : 
            leftItemBox = item.find(class_="vs_list vs_list1").find(class_="inner")
            global leftScore
            try :
                leftScore = leftItemBox.find("div", class_="score").stripped_strings
                leftScore = ("".join(leftScore))
            except :
                leftScore = 0
            leftName = leftItemBox.find("span", class_="name").text
            leftPitcher = leftItemBox.find_all("span")[2].text

            rightItemBox = item.find(class_="vs_list vs_list2").find(class_="inner")
            global rightScore
            try :
                rightScore = rightItemBox.find("div", class_="score").stripped_strings
                rightScore = ("".join(rightScore))
            except :
                rightScore = 0
            rightName = rightItemBox.find("span", class_="name").text
            rightPitcher = rightItemBox.find_all("span")[2].text
            bot.send_message(id, f"(선발 : {leftPitcher})\t {leftName}\t {leftScore} vs {rightScore}\t {rightName}\t (선발 : {rightPitcher})")
            time.sleep(3)
    

weather()
scrap_news()
sports_news()
print("시작")