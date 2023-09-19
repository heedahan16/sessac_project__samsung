import requests
from bs4 import BeautifulSoup
import re
import json

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
}

response = requests.get("https://news.naver.com/main/list.nhn?mode=LPOD&mid=sec&oid=001", headers=headers)
beautiful = (response.text, "html.parser")
beautiful = BeautifulSoup(response.text, "html.parser")

oid = {
    "뉴스1": "421"
    , "뉴시스": "003"
    , "연합뉴스": "001"
    , "연합뉴스TV": "422"
    , "연합뉴스 TV": "422"
    , "채널A": "449"
    , "한국경제TV": "215"
    , "JTBC": "437"
    , "KBS": "056"
    , "MBC": "214"
    , "MBN": "057"
    , "SBS": "055"
    , "SBS Biz": "374"
    , "TV조선": "448"
    , "YTN": "052"
}

oid = oid["연합뉴스"]

year = 2023

month = 8
if month < 10:
    month = "0" + str(month)
else:
    month = str(month)

for date in range(1, 32):
    if date < 10:
        date = "0" + str(date)
    else:
        date = str(date)

    date = str(year) + str(month) + str(date)
    print("date: ", date)

    page = 1

    while True:

        print("page: ", page)

        params = {
            "mode":"LPOD"
            , "mid":"sec"
            , "oid": oid
            , "date": date
            , "page": page
        }

        respon = requests.get("https://news.naver.com/main/list.naver", params=params, headers=headers)
        soup = BeautifulSoup(respon.text, "html.parser")

        now_page = int(soup.select_one("div.paging strong").text)

        if page != now_page:
            break

        for dl in soup.select("div.list_body ul li dl"):
            if dl.select_one("dt.photo a") != None:
                article = dl.select_one("dt.photo a").attrs["href"]
            else:
                article = dl.select_one("dt a").attrs["href"]

            print(article)    

            res = requests.get(article, headers=headers)
            bs = BeautifulSoup(res.text, "html.parser")

            try:
                # 일반 기사
                title = bs.select_one("div#ct h2").text
                content = bs.select_one("article#dic_area")
                    
            except:
                try:
                    # 스포츠 기사
                    title = bs.select_one("div.news_headline h4").text
                    content = bs.select_one("div#newsEndContents")
                    # print(title)
                    # print(content)
                # except:
                #     print("None!!!!!!!!!!!!!!!!!!!!!!")
                #     try :
                #         title = bs.select_one("div#content h2").text.replace("\n", "").strip()
                #         content = bs.select_one("div#contents article.dic_area")
                #     except:
                #         print("what theeeeeeeeeeeeeeeeee!")
                #         try:
                #             content = bs.select_one("div.end_body_wrp div#articBody")
                #         except:
                #             content = bs.select_one("div.end_body_wrp")
                except:
                    try:
                        title = bs.select_one("div#content h2").text.replace("\n", "").strip()
                        # content = bs.select_one("div#contents article.dic_area")
                    
                        content = bs.select_one("div.end_body_wrp div#articBody")
                    except:
                        content = bs.select_one("div.end_body_wrp")

            content = str(content)

            reg = re.finditer("(.{3}=연합뉴스\)).*[a-zA-Z0-9]\@[a-zA-Z]*\.[a-zA-Z]*\.[a-zA-Z]*", content)
        

            url = "https://news.like.naver.com/v1/search/contents?q=NEWS%5Bne_001_{}%5D".format(article[-10:])
            RES = requests.get(url, headers=headers)
            data = json.loads(RES.text)
            label = data["contents"][0]["reactionTextMap"]["ko"]

            for i in range(len(data["contents"][0]["reactions"])):
                reaction = data["contents"][0]["reactions"][i]["reactionType"]
                count = data["contents"][0]["reactions"][i]["count"]
                print(label[f"{reaction}"], count)

        page += 1

