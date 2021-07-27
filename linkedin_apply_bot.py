# automatically apply for jobs posted on linkedin (only if quick apply is available)

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time

URL = "URL OF A LINKEDIN SEARCH"

ACCOUNT_EMAIL = "YOUR EMAIL"
ACCOUNT_PASSWORD = "YOUR PASSWORD"
PHONE_NO = "YOUR PHONE NUMBER"

chrome_driver_path = "chromedriver.exe"
driver = webdriver.Chrome(chrome_driver_path)
driver.get(URL)

# time.sleep high, to not get detected as bot
time.sleep(2)
# log into linkedin
sign_in_button = driver.find_element_by_link_text("Sign in")
sign_in_button.click()

time.sleep(5)
# enter your credentials
email_field = driver.find_element_by_id("username")
email_field.send_keys(ACCOUNT_EMAIL)
password_field = driver.find_element_by_id("password")
password_field.send_keys(ACCOUNT_PASSWORD)
password_field.send_keys(Keys.ENTER)

time.sleep(5)

# find all job listings on the page
jobs = driver.find_elements_by_css_selector(".job-card-container--clickable")

for job in jobs:
    # click on each job listing
    job.click()
    time.sleep(2)
    try:
        # try to apply
        apply_button = driver.find_element_by_css_selector(".jobs-s-apply button")
        apply_button.click()

        time.sleep(5)
        # find a mobile phone field and enter your mobile phone number
        phone = driver.find_element_by_class_name("fb-single-line-text__input")
        if phone.text == "":
            phone.send_keys(PHONE_NO)

        submit_button = driver.find_element_by_css_selector("footer button")
        # check for additional field for application
        if submit_button.get_attribute("data-control-name") == "continue_unify":
            close_button = driver.find_element_by_class_name("artdeco-modal__dismiss")
            close_button.click()

            time.sleep(2)
            discard_button = driver.find_elements_by_class_name("artdeco-modal__confirm-dialog-btn")[1]
            #discard_button = driver.find_element_by_css_selector(".artdeco-modal__actionbar .artdeco-button--primary")
            discard_button.click()
            continue
        else:
            submit_button.click()

        time.sleep(2)
        close_button = driver.find_element_by_class_name("artdeco-modal__dismiss")
        close_button.click()

    # selenium exceptions if element wasn't found
    except NoSuchElementException:
        print("No application button!")
        continue

time.sleep(5)
driver.quit()

