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

    print(soup)