import telegram
import requests
from bs4 import BeautifulSoup
import schedule
import time

bot = telegram.Bot(token = "5433279502:AAF1snTj1bPTAjLwYj5BFfvgsZKDvN7tT84")
id = '@AlarmBotmadeEunbae'
eun_id = 5085254544

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
                    "[오늘의 날씨 알려드립니다.] \n"  +
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
        time.sleep(10)
    
def baseball_match() :
    url = "https://sports.news.naver.com/kbaseball/index"
    soup = create_soup(url)


    kboMatch = soup.find_all("div", id="_tab_box_kbo")[0]
    kboMatchItems = kboMatch.find("div", class_="hmb_list").find_all("li", class_="hmb_list_items")
    bot.send_message(id, "[야구 경기 예정]\n")
    for item in kboMatchItems : 
            leftItemBox = item.find(class_="vs_list vs_list1").find(class_="inner")
            global leftScore
            try :
                leftScore = leftItemBox.find("div", class_="score").stripped_strings
                leftScore = ("".join(leftScore))
            except :
                leftScore = " "
            leftName = leftItemBox.find("span", class_="name").text
            leftPitcher = leftItemBox.find_all("span")[2].text

            rightItemBox = item.find(class_="vs_list vs_list2").find(class_="inner")
            global rightScore
            try :
                rightScore = rightItemBox.find("div", class_="score").stripped_strings
                rightScore = ("".join(rightScore))
            except :
                rightScore = " "
            rightName = rightItemBox.find("span", class_="name").text
            rightPitcher = rightItemBox.find_all("span")[2].text
            bot.send_message(id, f"{leftName}\t (선발 : {leftPitcher})\t {leftScore}\n \tvs\n{rightName}\t (선발 : {rightPitcher})\t {rightScore}")
            time.sleep(3)
            

def baseball_result() :
    url = "https://sports.news.naver.com/kbaseball/index"
    soup = create_soup(url)


    kboMatch = soup.find_all("div", id="_tab_box_kbo")[0]
    kboMatchItems = kboMatch.find("div", class_="hmb_list").find_all("li", class_="hmb_list_items")
    bot.send_message(id, "[야구 경기 결과]\n")
    for item in kboMatchItems : 
            leftItemBox = item.find(class_="vs_list vs_list1").find(class_="inner")
            global leftScore
            try :
                leftScore = leftItemBox.find("div", class_="score").stripped_strings
                leftScore = ("".join(leftScore))
            except :
                leftScore = " "
            leftName = leftItemBox.find("span", class_="name").text

            rightItemBox = item.find(class_="vs_list vs_list2").find(class_="inner")
            global rightScore
            try :
                rightScore = rightItemBox.find("div", class_="score").stripped_strings
                rightScore = ("".join(rightScore))
            except :
                rightScore = " "
            rightName = rightItemBox.find("span", class_="name").text
            bot.send_message(id, f"{leftName}\t : {leftScore}\n \tvs\n{rightName}\t : {rightScore}")
            time.sleep(3)
            
def football() :
    url = "https://sports.news.naver.com/wfootball/index"
    soup = create_soup(url)
    day = soup.find("span", attrs={"class" : "inner"}).find_all("span", limit=1)
    for days in day :
        bot.send_message(eun_id, f"{days.get_text()} 경기 일정") # 08.06(토)
    
    Match = soup.find("div", class_ = "hmb_list").find_all("li", class_="hmb_list_items")
    for Matchs in Match :
        LeftBox = Matchs.find(class_ ="vs_list vs_list1").find(class_="inner")
        global LeftScore
        try :
            LeftScore = LeftBox.find("div", class_="score").stripped_strings
            LeftScore = ("".join(LeftScore))
        except :
            LeftScore = " "
        LeftTeam = LeftBox.find("span", class_ = "name").text
        
        RightBox = Matchs.find(class_="vs_list vs_list2").find(class_="inner")
        global RightScore
        try :
            RightScore = RightBox.find("div", class_="score").stripped_strings
            RightScore = ("".join(RightScore))
        except :
            RightScore = " "
        RightTeam = RightBox.find("span", class_ = "name").text
        Matchtime = Matchs.find(class_="state").text
        Matchtime = Matchtime.replace("\n", "")
        bot.send_message(eun_id, text = 
                        f"(경기시간 : {Matchtime}) \n" +
                        f"{LeftTeam} : {LeftScore} vs {RightScore} : {RightTeam}")
        time.sleep(10)

def sports_news() :
    url = "https://sports.news.naver.com/wfootball/index"
    world_football_url = "https://sports.news.naver.com/"
    soup = create_soup(url)
    
    sports = soup.find("ul", attrs={"class" : "home_news_list"}).find_all("li")
    for index, news in enumerate(sports) :
        title = news.find("a").get_text().strip()
        link = world_football_url + news.find("a")['href']
        bot.send_message(eun_id, text =
                         "[오늘의 해외축구] \n" +
                         (f"{index+1}. {title}\n") +
                         (f"    (링크 : {link})")
        )
        time.sleep(10)

schedule.every().day.at("05:50:00").do(weather)
schedule.every().day.at("07:30:00").do(scrap_news)
schedule.every().day.at("08:0:00").do(sports_news) #Eun
schedule.every().day.at("16:00:00").do(baseball_match)
schedule.every().day.at("18:00:00").do(football) #Eun
schedule.every().day.at("22:30:00").do(baseball_result)


while True :
    schedule.run_pending()
    time.sleep(90)