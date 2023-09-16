import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
}

response = requests.get("https://news.naver.com/main/officeList.naver", headers=headers)
beautiful = (response.text, "html.parser")

print(beautiful)

oid = "001"

respon = requests.get("https://news.naver.com/main/list.nhn?mode=LPOD&mid=sec&oid=" + oid, headers=headers)
soup = BeautifulSoup(respon.text, "html.parser")


print(soup.select("div#groupOfficeList table.group_table"))

for day in range(1, 32):
    if day < 10:
        day = "0" + str(day)
    date = "202308" + str(day)
    
    res = requests.get("https://news.naver.com/main/list.naver?mode=LPOD&mid=sec&oid=001&date=" + str(date), headers=headers)
    bs = BeautifulSoup(res.text, "html.parser")
    
    # print(bs.select("ul.type06_headline li dl"))