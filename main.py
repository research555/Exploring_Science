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
from pdb import set_trace
from exceptions import *


"""
STEPS

MAKE A LIST OF ALL UNIVERSITIES
1. OPEN AND LOG INTO RESEARCHGATE

2. NAVIAGTE TO INSTITUTIONS DIRECTORY

GATHERING PUBLICATIONS

1. I think the best way to do it would be to append all values to a string with delimiter '%%%' in sql
then use split.delimiter('%%%') to listify it when retrieving for NLP, links are separated with &&&

2. DO NOT LOG IN!! all details are given if youre not logged in for some reason.
"""

# # # # Load Important Things # # # #
cursor, mydb = DbAuth()
username = os.getenv('RG_USER')
password = os.getenv('RG_PASSWORD')

# # # # Log Into ResearchGate # # # #

#Login()

# # # # Cycle through universities on db and find their member numbers and if the links work # # # #
set_trace()

sql = "SELECT institution, link, tried, members_link FROM universities WHERE tried = 0"
cursor.execute(sql)
universities = cursor.fetchall()

for row in universities:
    university, link, tried, members_link = row[0], row[1], row[2], row[3]
    if tried == 0:
        driver.get(members_link)
        current_url = driver.current_url
        time.sleep(2)
        try:
            if current_url == members_link:
                sql = "UPDATE universities SET tried = 1 WHERE members_link = %s"
                cursor.execute(sql, (members_link,))
                #mydb.commit()
                time.sleep(2)
                heading = driver.find_elements(By.CLASS_NAME,
                                               'nova-legacy-c-nav__item-label')  # finds navbar with member number
                sql = "UPDATE universities SET success = 1 WHERE members_link = %s"
                cursor.execute(sql, (members_link,))
                # mydb.commit()
                num_pages, member_number = GetPageAndMemberNumber(login=False, university=university)
                print(f'added member number: ({member_number}) for {university} on universities db')

            else:
                raise UniversityLinkDoesNotExist

        except Exception as e:
            if UniversityLinkDoesNotExist:
                pass






"""

sql = 'SELECT link FROM profiles WHERE pub_scraped = 0'
cursor.execute(sql)
profile_links = cursor.fetchall()
for link in profile_links:
    link = link[0]
    number_articles = HasPublications(public=True)
    pub_number, pub_names, pub_links = GetPublications(public=False, number_articles=number_articles)
    sql = "UPDATE profiles SET pub_names = %s, pub_links = %s, pub_number = %s, pub_scraped = 1 WHERE link = %s"
    cursor.execute(sql, (pub_names, pub_links, pub_number, link,))
    mydb.commit()



sql = 'SELECT link from profiles'
    cursor.execute(sql)
    profiles = cursor.fetchall()
    for profile in profiles:
        profile = profile[0]
        RUN PUBLICATION SCRAPER FUNC
"""
                # scrape one link put into database DONE
                # scrape xp and education into database
                # repeat 1 million times
                # make graphical interface
