# play cookie clicker automatically

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

chrome_driver_path = "chromedriver.exe"
driver = webdriver.Chrome(executable_path=chrome_driver_path)

driver.get("http://orteil.dashnet.org/experiments/cookie/")
cookie = driver.find_element_by_id("cookie")
items = driver.find_elements_by_css_selector("#store div")

# get names of items
items_id_list = []
for item in range(len(items)-2, -1, -1):
    item_id = items[item].get_attribute("id")
    items_id_list.append(item_id)


running = True
# run 5 seconds
while running:
    time_end = time.time() + 5
    while time.time() < time_end:
        cookie.click()
# check how much money and buy the most expensive option
    for element in items_id_list:
            current_money = int(driver.find_element_by_id("money").text.replace(",", ""))
            item_cost = int(driver.find_element_by_id(element).text.replace("\n", "-").split("-")[1].replace(",", ""))
            if current_money >= item_cost:
                to_buy = driver.find_element_by_id(element)
                to_buy.click()
                break

## alternative: always buy everything possible
# running = True
# while running:
#     time_end = time.time() + 5
#     while time.time() < time_end:
#         cookie.click()
#
#     for element in items_id_list:
#         enough_money = True
#         while enough_money:
#             current_money = int(driver.find_element_by_id("money").text)
#             item_cost = int(driver.find_element_by_id(element).text.replace("\n", "-").split("-")[1].replace(",", ""))
#             if current_money >= item_cost:
#                 to_buy = driver.find_element_by_id(element)
#                 to_buy.click()
#             else:
#                 enough_money = False


driver.quit()


