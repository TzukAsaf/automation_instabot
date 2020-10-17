from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
#from easygui import passwordbox
import requests
import re
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException



options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(executable_path="C:\Program Files (x86)\chromedriver.exe", options=options)
driver.get("https://www.instagram.com/")


time.sleep(1)

went_wrong = True
while went_wrong:
    try:
        went_wrong = False
        user_name = input("Enter your User Name: ")
        driver.find_element_by_name("username").send_keys(user_name)
        user_pass = input("Enter your Password: ")
        driver.find_element_by_name("password").send_keys(user_pass)
        login = driver.find_element_by_xpath(
            "/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[3]/button/div")
        login.click()
        time.sleep(4)

        driver.execute_script("arguments[0].click();", driver.find_element_by_xpath(
            "/html/body/div[1]/section/main/div/div/div/div/button"))  # To get rid of the "save your logging info" pop-up
        time.sleep(1)

    except (NoSuchElementException, ElementClickInterceptedException):
        went_wrong = True
        driver.find_element_by_name("username").send_keys(Keys.CONTROL + "a")
        driver.find_element_by_name("username").send_keys(Keys.DELETE)
        driver.find_element_by_name("password").send_keys(Keys.CONTROL + "a")
        driver.find_element_by_name("password").send_keys(Keys.DELETE)
        print("One of the inputs was wrong, try again...")

print("Logged in successfully")
time.sleep(1)
driver.execute_script("arguments[0].click();", driver.find_element_by_xpath(
    "/html/body/div[4]/div/div/div/div[3]/button[2]"))  # To get rid of the "turn on notification" pop-up

search_the_hashtag = driver.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[2]/input")
search_the_hashtag.send_keys("js_executor")
time.sleep(1)

search_the_hashtag.send_keys(Keys.RETURN)
search_the_hashtag.send_keys(Keys.ENTER)

time.sleep(1)
driver.execute_script("arguments[0].click();",
                      driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[3]/a"))
time.sleep(3)

ig_source = requests.get("https://www.instagram.com/js_executor/").text
comp = re.compile(".. Following")
following_amount = re.findall(comp, ig_source)
total_following = int(str(following_amount[0]).split()[0])

# for i in range(1, following + 1):
while True:
    starting_time = time.perf_counter()
    went_wrong = 0
    print("starting new round")
    for i in range(3):
        index = 1
        while index <= total_following:
            went_wrong = 0

            try:
                driver.execute_script("arguments[0].click();", driver.find_element_by_xpath(
                    "/html/body/div[4]/div/div/div[2]/ul/div/li[" + str(index) + "]/div/div[3]/button"))

                driver.find_element_by_xpath("/html/body/div[5]/div/div/div/div[3]/button[1]").click()
            except NoSuchElementException:
                print("something went wrong...")

            index += 1

        time.sleep(10)
        index = 1
        while index <= total_following:
            driver.find_element_by_xpath(
                "/html/body/div[4]/div/div/div[2]/ul/div/li[" + str(index) + "]/div/div[3]/button").click()
            index += 1

        time.sleep(10)
    ending_time = time.perf_counter()
    print(f"process took {ending_time - starting_time} seconds")

    time.sleep(900)
    print(f"waited {(time.perf_counter() - ending_time) / 60} minutes")
