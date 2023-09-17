import requests
from bs4 import BeautifulSoup
import re

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
}
response = requests.get("https://news.naver.com/main/list.nhn?mode=LPOD&mid=sec&oid=001", headers=headers)
beautiful = BeautifulSoup(response.text, "html.parser")

oid = {
    "뉴스1": "421"
    , "뉴시스": "003"
    , "연합뉴스": "001"
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
    print("page: ", page)

    while True:

        params = {
            "mode":"LPOD"
            , "mid":"sec"
            , "oid": oid
            , "date": date
            , "page": page
        }

        respon = requests.get("https://news.naver.com/main/list.naver", params=params, headers=headers)
        soup = BeautifulSoup(respon.text, "html.parser")

        now_page = soup.select_one("div.paging strong").text

        if now_page != page:
            break

    for dl in soup.select("div.list_body ul li dl"):
        if dl.select_one("dt.photo a") != None:
            article = dl.select_one("dt.photo a").attrs["href"]
            
            res = requests.get(article, headers=headers)
            bs = BeautifulSoup(res.text, "html.parser")

            # print(bs)
        

            
    page += 1



                











# 해당 일자 모든 페이지 불러오기 실패
# import requests
# from bs4 import BeautifulSoup

# headers = {
#     "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
# }

# response = requests.get("https://news.naver.com/main/list.nhn?mode=LPOD&mid=sec&oid=001", headers=headers)
# beautiful = BeautifulSoup(response.text, "html.parser")

# page = 1

# while True:

#     print("page: ", page)

#     oid = {
#         "뉴스1": "421"
#         , "뉴시스": "003"
#         , "연합뉴스": "001"
#         , "연합뉴스TV": "422"
#         , "채널A": "449"
#         , "한국경제TV": "215"
#         , "JTBC": "437"
#         , "KBS": "056"
#         , "MBC": "214"
#         , "MBN": "057"
#         , "SBS": "055"
#         , "SBS Biz": "374"
#         , "TV조선": "448"
#         , "YTN": "052"
#     }

#     oid = oid["연합뉴스"]

#     date = 20230801

#     # year = 2023

#     # month = 8
#     # if month < 10:
#     #     month = "0" + str(month)
#     # else:
#     #     month = str(month)

#     # for day in range(1, 32):
#     #     if day < 10:
#     #         day = "0" + str(day)
#     #     else:
#     #         day = str(day)

#     #     date = str(year) + str(month) + str(day)

#     print("date: ", date)

#     params = {
#             "mode":"LPOD"
#             , "mid" : "sec"
#             , "oid" : oid
#             , "date" : date
#             , "page" : page
#         }

#     respon = requests.get("https://news.naver.com/main/list.naver", params=params, headers=headers)
#     soup = BeautifulSoup(respon.text, "html.parser")

#     now_page = soup.select_one("div.paging strong").text
    
#     for dl in soup.select("ul.type06_headline li dl"):
#         print(dl.select_one("dt.photo") == None)
#         # print(dl.select_one("dt.photo a").attrs["href"])

#     if page != now_page:
#         break

#     # print(soup)

#     page += 1      

# print("크롤링 종료")