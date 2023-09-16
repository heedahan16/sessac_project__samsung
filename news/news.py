import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
}
response = requests.get("https://news.naver.com/main/list.nhn?mode=LPOD&mid=sec&oid=001", headers=headers)
beautiful = BeautifulSoup(response.text, "html.parser")

for day in range(1, 32):
    if day < 10:
        day = "0" + str(day)
    date = "202308" + str(day)
    print(date)
    respon = requests.get("https://news.naver.com/main/list.naver?mode=LPOD&mid=sec&oid=001&date=" + str(date), headers=headers)
    soup = BeautifulSoup(respon.text, "html.parser")
    
    print(soup)