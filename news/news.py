import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
}

response = requests.get("https://news.naver.com/main/list.nhn?mode=LPOD&mid=sec&oid=001", headers=headers)
beautiful = (response.text, "html.parser")

oid = {
    "뉴스1": "421"
    , "뉴시스": "003"
    , "연합뉴스": "001"
    , "연합뉴스TV": "422"
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

for day in range(1, 32):
    if day < 10:
        day = "0" + str(day)
    date = str(year) + str(month) + str(day)
    # print(date)
        
    url = "https://news.naver.com/main/list.nhn?mode=LPOD&mid=sec&oid={}&date={}".format(oid, date)
    respon = requests.get(url, headers=headers)
    soup = BeautifulSoup(respon.text, "html.parser")
    print(soup)
