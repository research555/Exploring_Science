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
import random

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

#Login()

# # # # Load Important Things # # # #
cursor, mydb = DbAuth()
username = os.getenv('RG_USER')
password = os.getenv('RG_PASSWORD')

# # # # Cycle through universities on db and find their member numbers and if the links work # # # #

sql = "SELECT institution, link, tried, members_link FROM universities WHERE tried = 0"
cursor.execute(sql)
universities = cursor.fetchall()
i = 0
for row in universities:
    i += 1
    print(i)
    university, link, tried, members_link = row[0], row[1], row[2], row[3]
    if tried == 0:
        SetTried(tried=1, university=university)
        driver.get(members_link)
        try:  # add unis location as a string, separate later
            location = driver.find_element(By.CLASS_NAME, 'institution-header-details-meta-items')
            location = location.text
        except Exception as e:  # no location
            location = 'Could not find location'
        finally:
            sql = 'UPDATE universities SET location = %s WHERE institution = %s'
            cursor.execute(sql, (location, university,))
            mydb.commit()

        current_url = driver.current_url
        hyphenated_members_link = members_link.replace('_', '-')
        hyphenated_link = link.replace('_', '-')
        link_possibilities = [link, members_link, hyphenated_link, hyphenated_members_link]
        time.sleep(random.randint(1, 4))

        try:
            if current_url in link_possibilities: # 4 different link combinations
                #UpdateLink(current_url=current_url, members_link=members_link)
                time.sleep(random.randint(1, 4))
                heading = driver.find_elements(By.CLASS_NAME,
                                               'nova-legacy-c-nav__item-label')  # finds navbar with member number
                if bool(heading):
                    SetSuccess(success=1, university=university)
                    num_pages, member_number = GetPageAndMemberNumber(login=False, university=university)
                    print(f'added member number: ({member_number}) for {university} on universities db\nLogging all profiles')
                    LogAllProfiles(num_pages=num_pages, university=university, current_url=current_url)
                    print(f'all profiles logged for the {university}')

                else:
                    SetSuccess(success=0, university=university)
                    time.sleep(random.randint(1, 4))

                    raise NoMembersButExists
            else:
                SetTried(tried=1, university=university)
                SetSuccess(success=0, university=university)
                time.sleep(random.randint(1, 4))

                raise UniversityLinkDoesNotExist

        except Exception as e:
            if UniversityLinkDoesNotExist: # handle later if needed
                sql = "UPDATE universities SET exceptions = %s WHERE institution = %s"
                cursor.execute(sql, ('UniversityLinkDoesNotExist', university,))
                mydb.commit()

            if NoMembersButExists:
                sql = "UPDATE universities SET exceptions = %s WHERE institution = %s"
                cursor.execute(sql, ('NoMembersButExists', university,))
                mydb.commit()

            else:
                pass
    else:
        pass
