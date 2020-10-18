from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
# from easygui import passwordbox
import requests
import re
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import keyboard


def followers_list():
    followers = []
    time.sleep(1)
    followersList = driver.find_element_by_xpath("/html/body/div[4]/div/div/div[2]")
    for user in followersList.find_elements_by_css_selector('li'):
        try:
            userLink = user.find_elements_by_css_selector('a')[1].get_attribute('title')
        except:
            userLink = user.find_element_by_css_selector('a').get_attribute('title')

        followers.append(userLink)
        return followers
def follow_person(username):
    # at the end you will be at your profile
    search_person = driver.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[2]/input")
    search_person.send_keys(str(username))
    time.sleep(1)
    search_person.send_keys(Keys.RETURN)
    search_person.send_keys(Keys.ENTER)
    time.sleep(2)
    driver.execute_script("arguments[0].click();",
                          driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[3]/a"))
    driver.execute_script("arguments[0].click();",
                          driver.find_element_by_xpath(
                              "/html/body/div[1]/section/main/div/header/section/div[1]/div[2]/div/div/div/span/span[1]/button"))
    driver.execute_script("arguments[0].click();",
                          driver.find_element_by_xpath(
                              "/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[5]/span"))
    driver.execute_script("arguments[0].click();",
                          driver.find_element_by_xpath(
                              "/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[5]/div[2]/div/div[2]/div[2]/a[1]/div/div[2]/div/div/div"))
    time.sleep(2)


options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(executable_path="C:\Program Files (x86)\chromedriver.exe", options=options)
driver.get("https://www.instagram.com/")

time.sleep(1)

went_wrong = True
while went_wrong:
    try:
        went_wrong = False
        user_name = input("Enter your Username: ")
        driver.find_element_by_name("username").send_keys("js_executor")
        user_pass = input("Enter your Password: ")
        driver.find_element_by_name("password").send_keys("abyssal2484551")
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

lst_all_followers = followers_list()
while not keyboard.is_pressed('q'):

    starting_time = time.perf_counter()
    went_wrong = 0
    print("starting new round")
    for i in range(3):
        index = 1
        while index <= total_following:  # unfollow
            went_wrong = 0

            try:
                driver.execute_script("arguments[0].click();", driver.find_element_by_xpath(
                    "/html/body/div[4]/div/div/div[2]/ul/div/li[" + str(index) + "]/div/div[3]/button"))

                driver.find_element_by_xpath("/html/body/div[5]/div/div/div/div[3]/button[1]").click()
            except (NoSuchElementException, ElementClickInterceptedException):
                print("something went wrong...")
                went_wrong = True
                break

            index += 1
        if went_wrong:
            break
        time.sleep(10)
        index = 1
        while index <= total_following:  # follow
            try:
                driver.find_element_by_xpath(
                    "/html/body/div[4]/div/div/div[2]/ul/div/li[" + str(index) + "]/div/div[3]/button").click()
                index += 1
            except (NoSuchElementException, ElementClickInterceptedException):
                went_wrong = True
                break
        if went_wrong:
            break
        time.sleep(10)
    if went_wrong:
        print("something went wrong")
        driver.refresh()
        break
    else:
        ending_time = time.perf_counter()
        print(f"session took {ending_time - starting_time} seconds")

        time.sleep(900)
        print(f"waited {(time.perf_counter() - ending_time) / 60} minutes")
driver.refresh()
time.sleep(4)
lst_current_followers = followers_list()
for user in lst_all_followers:
    if user not in lst_current_followers:
        follow_person(user)

