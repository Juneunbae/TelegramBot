import requests
from bs4 import BeautifulSoup
import time

def create_soup(url) :
    res = requests.get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    return soup

def football() :
    url = "https://sports.news.naver.com/wfootball/index"
    soup = create_soup(url)
    day = soup.find("span", attrs={"class" : "inner"}).find_all("span", limit=1)
    for days in day :
        print(f"{days.get_text()} 경기 일정") # 08.06(토)
    
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
        print(
        f"(경기시간 : {Matchtime}) \n" +
        f"{LeftTeam} : {LeftScore} vs {RightScore} : {RightTeam}"
        )
        time.sleep(15)