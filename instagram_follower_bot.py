
## follow on instagram

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException
import time

INTERESTING_ACCOUNT = "NAME OF ACCOUNT YOU WANT TO CHECK"
ACCOUNT_USER = "YOUR USERNAME"
ACCOUNT_PASSWORD = "YOUR PASSWORD"


chrome_driver_path = "chromedriver.exe"


class InstagramFollower:

    def __init__(self, driver):
        self.driver = webdriver.Chrome(executable_path=driver)

    def login(self):
        self.driver.get("https://www.instagram.com/accounts/login/")
        time.sleep(5)

        username = self.driver.find_element_by_name("username")
        password = self.driver.find_element_by_name("password")

        username.send_keys(ACCOUNT_USER)
        password.send_keys(ACCOUNT_PASSWORD)

        time.sleep(2)
        password.send_keys(Keys.ENTER)

    def find_followers(self):
        time.sleep(5)
        self.driver.get(f"https://www.instagram.com/{INTERESTING_ACCOUNT}")

        time.sleep(2)
        # access the follower list of the account you want to look into
        followers = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a')
        followers.click()

        time.sleep(2)
        # get all followers
        modal = self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[2]')
        # Scroll inside of popup div
        # thanks https://stackoverflow.com/questions/38041974/selenium-scroll-inside-of-popup-div
        for i in range(10):
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", modal)
            time.sleep(2)

    def follow(self):
        # get the "follow button" for each follower
        all_buttons = self.driver.find_elements_by_css_selector("li button")
        for button in all_buttons:
            try:
                # click follow
                button.click()
                time.sleep(1)
            # if no button available (because you already follow the user e.g.)
            except ElementClickInterceptedException:
                cancel_button = self.driver.find_element_by_xpath('/html/body/div[5]/div/div/div/div[3]/button[2]')
                cancel_button.click()


bot = InstagramFollower(chrome_driver_path)
bot.login()
bot.find_followers()
bot.follow()
