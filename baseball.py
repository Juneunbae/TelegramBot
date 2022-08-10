import requests
from bs4 import BeautifulSoup
import time

def create_soup(url) :
    res = requests.get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    return soup

def baseball_match() :
    url = "https://sports.news.naver.com/kbaseball/index"
    soup = create_soup(url)

    kboMatch = soup.find_all("div", id="_tab_box_kbo")[0]
    kboMatchItems = kboMatch.find("div", class_="hmb_list").find_all("li", class_="hmb_list_items")
    print("[야구 경기 예정]\n")
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
            print(f"{leftName}\t (선발 : {leftPitcher})\t {leftScore}\n \tvs\n{rightName}\t (선발 : {rightPitcher})\t {rightScore}")
            time.sleep(15)
            

def baseball_result() :
    url = "https://sports.news.naver.com/kbaseball/index"
    soup = create_soup(url)


    kboMatch = soup.find_all("div", id="_tab_box_kbo")[0]
    kboMatchItems = kboMatch.find("div", class_="hmb_list").find_all("li", class_="hmb_list_items")
    print("[야구 경기 결과]\n")
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
            print(f"{leftName}\t : {leftScore} \tvs\t {rightName}\t : {rightScore}")
            time.sleep(15)
            
def baseball_rank() :
    rank_url = "https://sports.news.naver.com/kbaseball/record/index?category=kbo"
    soup = create_soup(rank_url)

    selected = soup.find_all(id="regularTeamRecordList_table")[0]

    rows = selected.find_all("tr")
    print("[야구 순위]\n")
    for item in rows :
        # tr
        print(
                item.find_all("th")[0].text + "위 : "  # rank
                +item.find_all("div")[0].text # team name
                +"("
                +"경기수 : "+item.find_all("td")[1].text
                +"\t승 : "+item.find_all("td")[2].text
                +"\t패 : "+item.find_all("td")[3].text
                +"\t무 : "+item.find_all("td")[4].text
                +"\t승률 : "+item.find_all("td")[5].text
                +"\t게임차 : "+item.find_all("td")[6].text
                +"\t연승/연패 : "+item.find_all("td")[7].text
                +"\t최근10경기 : "+item.find_all("td")[10].text
                +")\n"
        )
        time.sleep(15)
    