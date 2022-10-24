from selenium import webdriver
from selenium.webdriver.common.by import By
from db_functions import DbAuth
import random
import math
from dotenv import load_dotenv
import os


load_dotenv()
driver = webdriver.Edge(os.getenv('EDGE_WEBDRIVER_PATH'))

single_card = 'dfc9e'

single = 'CybotCookiebotDialogBodyButton'
driver.get('https://no.unibet.com/betting/sports/home')

master_bar = driver.find_elements(By.CLASS_NAME, single)

for element in master_bar:
    if element.text == 'Allow all cookies':
        element.click()

def FindOdds():

    live_cards = driver.find_elements(By.CLASS_NAME, single_card)
    whole_list = []
    for ele in live_cards:
        team_odds = []
        odds = ele.find_elements(By.CLASS_NAME, '_3373b')
        teams = ele.find_elements(By.CLASS_NAME, '_59e1d')
        for team in teams:
            team_odds.append(team.text)
        for odd in odds:
            team_odds.append(odd.text)
        whole_list.append(team_odds)

    return whole_list

x = FindOdds()

print(x)
"""
master = driver.find_elements(By.XPATH, "//*")
for element in master:
    print(element.tag_name, element.get_attribute('class'))

driver.close()

"""