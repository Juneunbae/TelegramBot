import requests
from bs4 import BeautifulSoup
import time

def create_soup(url) :
    res = requests.get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    return soup

def sports_news() :
    url = "https://sports.news.naver.com/wfootball/index"
    world_football_url = "https://sports.news.naver.com/"
    soup = create_soup(url)
    
    sports = soup.find("ul", attrs={"class" : "home_news_list"}).find_all("li")
    for index, news in enumerate(sports) :
        title = news.find("a").get_text().strip()
        link = world_football_url + news.find("a")['href']
        print(
        "[오늘의 해외축구] \n" +
        (f"{index+1}. {title}\n") +
        (f"    (링크 : {link})")
        )
        time.sleep(15)