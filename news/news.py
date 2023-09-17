import requests
from bs4 import BeautifulSoup
import re

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

            res = requests.get(article, headers=headers)
            bs = BeautifulSoup(res.text, "html.parser")

            try:
                title = bs.select_one("div#ct h2").text
                content = bs.select_one("div#contents article#dic_area")
                
            except:
                try:
                    title = bs.select_one("div#content h4").text
                    content = bs.select_one("div#content div#newsEndContents")
                except:
                    title = bs.select_one("div#content h2").text.replace("\n", "").strip()
                    try:
                        content = bs.select_one("div.end_body_wrp div#articBody")
                    except:
                        content = bs.select_one("div.end_body_wrp")

            reg = "[a-zA-Z]* *ⓒ.*|<br\/><br\/> * |[a-zA-Z0-9]*@.*|<[^>]*>"
            content_reg = re.sub(reg, "", str(content)).replace("\n", "").strip()

        page += 1