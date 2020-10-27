from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

from bs4 import BeautifulSoup
import os
import requests
import getpass
#from easygui import passwordbox
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException

from selenium.webdriver.chrome.options import Options

import re


options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(executable_path="C:\Program Files (x86)\chromedriver.exe", options=options)
driver.get("https://www.instagram.com/")

sleep(1)



went_wrong = True
while went_wrong:
    try:
        went_wrong = False
        user_name = input("enter your username: ")
        driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[1]/div/label/input").send_keys(user_name)
        user_password = input("enter your password: ")

        driver.find_element_by_name("password").send_keys(user_password)
        login = driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[3]/button/div")
        login.click()
        sleep(4)
        driver.find_element_by_xpath(
            "/html/body/div[1]/section/main/div/div/div/div/button").click()  # To get rid of the "save your logging info" pop-up

    except (NoSuchElementException, ElementClickInterceptedException):
        went_wrong = True
        driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[1]/div/label/input").send_keys(Keys.CONTROL + "a")
        driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[1]/div/label/input").send_keys(Keys.DELETE)
        driver.find_element_by_name("password").send_keys(Keys.CONTROL + "a")
        driver.find_element_by_name("password").send_keys(Keys.DELETE)
        print("One of the inputs was wrong, try again...")


print("Logged in successfully")
sleep(1)
driver.execute_script("arguments[0].click();", driver.find_element_by_xpath(
    "/html/body/div[4]/div/div/div/div[3]/button[2]"))  # To get rid of the "turn on notification" pop-up

hashtag = input("Enter the hashtag you would like to like: ")
search_the_hashtag = driver.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[2]/input")
search_the_hashtag.send_keys("#" + hashtag)
sleep(1)
search_the_hashtag.send_keys(Keys.RETURN)
search_the_hashtag.send_keys(Keys.ENTER)


sleep(4)
post = driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div/div[1]/div[1]/a/div/div[2]").click()
sleep(2)
bug_counter = 0
liked_posts = 0


how_many = int(input("Enter integer that represent how many posts do you want to like: "))
while liked_posts != how_many:

    try:
        driver.execute_script("arguments[0].click();",
                      driver.find_element_by_xpath("/html/body/div[4]/div[2]/div/article/div[3]/section[1]/span[1]/button"))
        liked_posts += 1
        bug_counter = 0

        driver.execute_script("arguments[0].click();", driver.find_element_by_link_text("Next"))
        sleep(1)
    except NoSuchElementException:
        print("something went wrong, skipping to next post")
        driver.execute_script("arguments[0].click();", driver.find_element_by_link_text("Next"))
        bug_counter += 1
        if bug_counter > 10:
            break
        sleep(5)
    try:

        if liked_posts % 40 == 0:
            sleep(300)
            print("waited 5 minutes")

        if liked_posts % 20 == 0:
            sleep(1)
            driver.execute_script("arguments[0].click();", driver.find_element_by_xpath("/html/body/div[4]/div[3]/button"))
            driver.refresh()
            driver.execute_script("arguments[0].click();", driver.find_element_by_xpath(
                "/html/body/div[1]/section/main/article/div[2]/div/div[1]/div[1]/a/div/div[2]"))
            sleep(2)

    except NoSuchElementException:
        print("Error accrued, breaking the loop")
        break



print(f"{liked_posts} posts has been liked")


driver.quit()