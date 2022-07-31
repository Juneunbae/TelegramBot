import telegram
import requests
from bs4 import BeautifulSoup

bot = telegram.Bot(token = "5433279502:AAF1snTj1bPTAjLwYj5BFfvgsZKDvN7tT84")
id = '@AlarmBotmadeEunbae'
# so_id = 5083993056


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

    main_news = soup.find("ul", attrs={"class" : "press_news_list as_bottom"}).find_all("li")
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
       
    sports2 = soup.find("ul", attrs={"class" : "home_news_list division"}).find_all("li")
    for index2, news2 in enumerate(sports2) :
        title2 = news2.find("a").get_text().strip()
        link2 = world_football_url + news2.find("a")['href']
        bot.send_message(id, text =
                         "[오늘의 해외축구] \n" +
                         (f"{index2+11}. {title2} \n") +
                         (f"    (링크 : {link2})")
        )

weather()
scrap_news()
sports_news()
print("시작")