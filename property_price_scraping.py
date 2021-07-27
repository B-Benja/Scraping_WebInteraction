# get the listings, submit them to google form and store them in a google sheet (API would be more convenient;
# good practice for selenium

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time

property_website = "https://www.zillow.com/homes/San-Francisco,-CA_rb/"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Safari/605.1.15",
    "Accept-Language": "en-US"
}


# first scrape the data from the property website
response = requests.get(property_website, headers=headers)
print(response)
soup = BeautifulSoup(response.text, "html.parser")

# get all listings
data = soup.find_all("article", {"class": "list-card"})
del data[-1] # last entry on website is not a listing
# print(data)

# scrape prices, links to listings & addresses; store them in list
listings = []

for e in data:
    price = e.find("div", {"class": "list-card-price"}).text
    link = e.find("a").attrs['href']
    address = e.find("address").text
    listings.append(
        {"link": link,
         "price": price,
         "address": address,}
    )


# fill the data into google forms
# needed to add data into form (can be done with google's API, but I want to learn more about selenium)
chrome_driver_path = "chromedriver.exe"
driver = webdriver.Chrome(executable_path=chrome_driver_path)


for n in range(len(listings)):
    driver.get(YOUR GOOGLE FORM LINK)

    time.sleep(2)
    address = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit_button = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div')

    address.send_keys(listings[n]["address"])
    price.send_keys(listings[n]["price"])
    link.send_keys(listings[n]["link"])
    submit_button.click()

driver.quit()


