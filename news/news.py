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
                    title = bs.select_one("div#content h4").text
                    content = bs.select_one("div#newsEndContents")
                    

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
                    title = bs.select_one("div#content h2").text.replace("\n", "").strip()
                    content = bs.select_one("div#contents article.dic_area")
                    # try:
                    #     content = bs.select_one("div.end_body_wrp div#articBody")
                    # except:
                    #     content = bs.select_one("div.end_body_wrp")

            content = str(content)

            p = "<p.*>.*<\/p>"
            br = "<br\/> *"
            offer = "\[.*\]"
            day = "[0-9]+\.+[0-9].[0-9].?"
            email = "[a-zA-Z0-9]*@[a-zA-Z]*\.[a-zA-Z]*\.[a-zA-Z]*+"
            info = "<!.*>"
            slogan = ".*연합뉴스\)"
            reporter = ".* =|.reporter.+|profile.*|<*name.*>"
            summary = "<[^\>]*><\/.*>"
            a = "<a.*>.*<\/a>"
            em = "<em.*>.*"
            button = "<button.*>.*<\/button>.*"
            tag = "<[^\>]*>"
            content = re.sub(p, "", content)
            content = re.sub(br, "", content)
            content = re.sub(offer, "", content)
            content = re.sub(day, "", content)
            content = re.sub(email, "", content)
            content = re.sub(info, "", content)
            content = re.sub(reporter, "", content)
            content = re.sub(slogan, "", content)
            content = re.sub(summary, "", content)
            content = re.sub(a, "", content)
            content = re.sub(em, "", content)
            content = re.sub(button, "", content)
            content= re.sub(tag, "", content)

            # print("title: ", title)
            # print("content: ",content.replace("\n", "").replace(" , 닫기구독자응원수", "").replace("닫기구독자응원수가이드 닫기", "").replace("S&amp;P", "S&P").strip())
    
            res = requests.get("https://sports.like.naver.com/v1/search/contents?suppress_response_codes=true&callback=jQuery111304373371927169414_1695020995540&q=SPORTS%5Bne_001_0014106287%5D%7CJOURNALIST%5B56735(period)%5D%7CSPORTS_MAIN%5Bne_001_0014106287%5D&isDuplication=false&cssIds=MULTI_PC%2CSPORTS_PC&_=1695020995541", headers=headers)

            data = re.finditer("{.+}", res.text)
            for datum in data:
                # print(datum.group())

                result = json.loads(datum.group())
                reaction = result["contents"][0]["reactions"][0]["reactionType"]
                count = result["contents"][0]["reactions"][0]["count"]
                print(reaction, count)
            
        page += 1

