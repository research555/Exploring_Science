from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from functions import *
import os
from dotenv import load_dotenv
import country_converter as coco
import pandas as pd
import time
import regex
import math


"""
STEPS

MAKE A LIST OF ALL UNIVERSITIES
1. OPEN AND LOG INTO RESEARCHGATE

2. NAVIAGTE TO INSTITUTIONS DIRECTORY

"""

# # # # Load Important Things # # # #

cursor, mydb = db_auth()
username = os.getenv('RG_USER')
password = os.getenv('RG_PASSWORD')
driver = webdriver.Edge(executable_path='C:/Users/imran/PycharmProjects/Exploring_Science/Driver/msedgedriver.exe')

# # # # Log Into ResearchGate # # # #

login(driver=driver, username=username, password=password)

university = 'University-of-Bergen'
driver.get(f'https://www.researchgate.net/institution/{university}/members')
heading = driver.find_elements(By.CLASS_NAME, 'nova-legacy-c-nav__item-label') # finds navbar with member number

for elements in heading:
    text = elements.text.lower()
    if 'members' in text:
        number_members = regex.findall(r'[0-9]', text)
        number_members = int(''.join(number_members)) # remove commas
        num_pages = math.ceil(number_members/10)  # 10 profiles per page

        iter = 1
        for pages in range(num_pages):
            driver.get(f'https://www.researchgate.net/institution/{university}/members/{pages}')
            profile = driver.find_elements(By.CLASS_NAME, 'institution-members-list')
            for x in profile:
                link = x.find_element(By.CLASS_NAME, 'nova-legacy-e-link--theme-bare').get_attribute('href')
                print(f'loop {iter}')
                LogProfiles(driver=driver, university=university)
                iter += 1




                # scrape one link put into database DONE
                # scrape xp and education into database
                # repeat 1 million times
                # make graphical interface
