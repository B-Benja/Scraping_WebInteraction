#### watch certain stock and send top 3 news articles if stock prices change by 5%

import datetime
import smtplib
import requests
from datetime import date

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
API_STOCK = "https://www.alphavantage.co/query"
API_KEY_STOCK = "API KEY"
API_NEWS = "https://newsapi.org/v2/everything"
API_KEY_NEWS = "API KEY"
MY_EMAIL = "YOUR EMAIL"
MY_SMTP = "smtp.gmail.com"
PASSWORD = "YOUR PASSWORD"

## When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
# https://www.alphavantage.co/documentation/
PARAMETERS_STOCK = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": API_KEY_STOCK
}

stock_price = requests.get(API_STOCK, params=PARAMETERS_STOCK).json()

# get date yesterday and day before yesterday
yesterday = date.today() - datetime.timedelta(days=1)
before_yesterday = date.today() - datetime.timedelta(days=2)

yesterday_price = float(stock_price["Time Series (Daily)"][f"{yesterday}"]["4. close"])
before_yesterday_price = float(stock_price["Time Series (Daily)"][f"{before_yesterday}"]["4. close"])

difference = abs(yesterday_price - before_yesterday_price)
difference_percentage = (difference / yesterday_price) * 100

## get the first 3 news pieces for the COMPANY_NAME
# from https://newsapi.org/
PARAMETERS_NEWS = {
    "qInTitle": COMPANY_NAME,
    "from": yesterday,
    "apiKey": API_KEY_NEWS,
}

news_data = requests.get(API_NEWS, params=PARAMETERS_NEWS).json()

# function to extract news
def get_news():
    email_content = ""
    for article in range(0, 3):
        email_content += news_data["articles"][article]["title"] + "\n" + news_data["articles"][article][
            "description"] + "\n" + news_data["articles"][article]["url"] + "\n\n"
    return email_content

# to send email
def send_email(header, email_content):
    with smtplib.SMTP(MY_SMTP) as email:
        email.starttls()
        email.login(user=MY_EMAIL, password=PASSWORD)
        email.sendmail(from_addr=MY_EMAIL, to_addrs=MY_EMAIL,
                       msg=f"Subject:{header}\n\n{email_content.encode('utf-8')}")

print(difference_percentage)
## send results to my email
# Send a seperate message with the percentage change and each article's title and description to your mail box
if difference_percentage > 5:
    header = f"{STOCK}: {round(difference_percentage, 1)}%"
    send_email(header, get_news())
