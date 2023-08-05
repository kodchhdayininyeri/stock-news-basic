import requests

import smtplib

MY_EMAIL="YOUR EMAIL"
PASSWORD="YOUR PASSWORD"

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"


STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

API_KEY_ALPHAVANTAGE= "VPHIM0YWGGCK3ME2"
NEWS_API_KEY = "8c3f3c53c67d4a5788df975b09033f4b"
PARAMS_ALPHAVANTAGE = {
    "function":"TIME_SERIES_DAILY",
    "symbol":STOCK_NAME,
    "apikey":API_KEY_ALPHAVANTAGE
}

data=requests.get(STOCK_ENDPOINT,params=PARAMS_ALPHAVANTAGE)
data.raise_for_status()
data = data.json()['Time Series (Daily)']
data_list = [value for (key,value) in data.items()]




yesterday_sprice = float(data_list[0]["4. close"])
before_yesterday_sprice = float(data_list[1]["4. close"])



difference_price = (yesterday_sprice-before_yesterday_sprice)
up_or_down_emoji = None
if difference_price > 0:
    up_or_down_emoji= "🔼"
else:
    up_or_down_emoji = "🔽"

diff_percent=round((difference_price/before_yesterday_sprice)*100)


if abs(diff_percent) > 0:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle" : COMPANY_NAME,
    }
    new_response=requests.get(NEWS_ENDPOINT,params=news_params)

    articles = new_response.json()["articles"][:3]

    formatted_articles = [f"Headline: {article['title']}.\nBrief: {article['description']}" for article in articles]


for article in formatted_articles:
    connection = smtplib.SMTP("smtp.gmail.com",port=587)
    connection.starttls()
    connection.login(user=MY_EMAIL,password=PASSWORD)
    subject = f"{STOCK_NAME}: {up_or_down_emoji}".encode('utf-8')  # Encode subject as UTF-8
    msg = f"Subject: {subject.decode('utf-8')}\n\n{article}"  # Decode subject back to Unicode

    connection.sendmail(from_addr=MY_EMAIL,
                        to_addrs=MY_EMAIL,
                        msg=msg.encode('utf-8'))
    connection.close()

