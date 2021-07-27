# check for prices on amazon and get an email if price is below target price

import requests
from bs4 import BeautifulSoup
import smtplib

website = "YOUR AMAZON LINK"
headers = {
    'authority': 'www.amazon.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'dnt': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-dest': 'document',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
}


SMTP = "smtp.gmail.com"
MY_EMAIL = ""
MY_PASSWORD = ""

TARGET_PRICE = 100

response = requests.get(website, headers=headers)
print(response)
soup = BeautifulSoup(response.text, "lxml")
price_str = soup.find("span", id="priceblock_ourprice").text
price = float(price_str.split()[0].replace(",", "."))
product = soup.find("span", id="productTitle").text.replace("\n", "")

if price < TARGET_PRICE:
    with smtplib.SMTP(host=SMTP) as email:
        email.starttls()
        email.login(MY_EMAIL, MY_PASSWORD)
        email.sendmail(from_addr=MY_EMAIL,
                       to_addrs=MY_EMAIL,
                       msg=f"Subject: Price alarm\n\nThe price for\n{product}\ndropped to {price}!")
else:
    print(f"{product}\nis still too expensive! ({price - TARGET_PRICE} Euros above target price)")
