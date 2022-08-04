import requests
from bs4 import BeautifulSoup

def create_soup(url) :
    res = requests.get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    return soup

def scrap_news() :
    url = "https://media.naver.com/press/001"
    soup = create_soup(url)

    main_news = soup.find("ul", attrs={"class" : "press_news_list as_bottom"}).find_all("li")
    for index, news in enumerate(main_news) :
        title = news.find("a").get_text().strip()
        link = news.find("a")["href"]
        print(
            "[오늘의 뉴스] \n" +
            (f"{index + 1}. {title} \n") +
            (f"    (링크 : {link})")
        )