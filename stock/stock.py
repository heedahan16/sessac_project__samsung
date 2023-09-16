import requests
from bs4 import BeautifulSoup

response = requests.get("https://finance.naver.com/item/sise.nhn?code=005930")
beautiful = BeautifulSoup(response.text, "html.parser")

stock = []

page = 1
while page < 5:

    url = "https://finance.naver.com/item/sise_day.naver?code=005930&page=" + str(page)

    page += 1

    headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
}
    respon = requests.get(url, headers=headers)
    soup = BeautifulSoup(respon.text, "html.parser")

    for tr in soup.select("tr"):
        if (tr.select_one("span") != None) and (tr.select_one("span").text[:7]) == "2023.08":
            date = tr.select_one("span").text
            close_price = tr.select("span.tah.p11")[0].text
            up_down = tr.select("span.tah.p11")[1].text.replace("\n", "").strip()
            open_price = tr.select("span.tah.p11")[2].text
            high_price = tr.select("span.tah.p11")[3].text
            low_price = tr.select("span.tah.p11")[4].text
            volume = tr.select("span.tah.p11")[5].text

            stock.append({
                "날짜": date
                , "종가": close_price
                , "전일비": up_down
                , "시가": open_price
                , "고가": high_price
                , "저가": low_price
                , "거래량": volume
            })            

print(stock)


import json
stock
with open("stock.json", "w", encoding="utf-8-sig") as f:
    json.dump(stock, f, ensure_ascii = False)

import csv

with open("stock.json", "r", encoding="utf-8-sig") as input_file, open("stock.csv", "w", newline="") as output_file:
    data = json.load(input_file)

    f = csv.writer(output_file)

    for datum in data:
        f.writerow([datum["날짜"], datum["종가"], datum["전일비"], datum["시가"], datum["고가"], datum["저가"], datum["거래량"]])
    