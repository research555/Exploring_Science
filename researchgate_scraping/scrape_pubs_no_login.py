import random
import time
from functions import *
import pdb
from selenium import webdriver
from selenium.webdriver.common.by import By
import regex as re

# list size max 100 for some reason..
# function doesnt work for get pubs
# some pubs are hidden and wont be scraped
# 2 seconds per profile currently, 2 min per 100

cursor, mydb = DbAuth()
sql = 'SELECT link FROM profiles WHERE institution = "Universidad_de_Buenos_Aires" AND pub_scraped = 0'
cursor.execute(sql)
profile_links = cursor.fetchall()
i = 1

driver.get('https://www.researchgate.net')
time.sleep(3)
accept = driver.find_element(By.CLASS_NAME, 'css-1u05hh5')
accept.click()  # Accepts cookies
time.sleep(1)

for link in profile_links:
    print(f'iteration #{i}')
    link = link[0]
    driver.get(link)
    public = IsPublic(link)
    time.sleep(random.randint(3,8))
    if public is True:
        sections = driver.find_elements(By.CLASS_NAME, 'nova-legacy-c-card__header')
        for section in sections:
            if 'publication' in section.text.lower():
                number_articles = re.findall('[0-9]+', section.text)
                print(number_articles)
                if bool(number_articles):
                    pub_number, pub_names, pub_links = GetPublications(public=True, number_articles=number_articles, profile_link=link)
                    sql = "UPDATE profiles SET pub_titles = %s, pub_links = %s, pub_number = %s, pub_scraped = 1 WHERE link = %s"
                    cursor.execute(sql, (pub_names, pub_links, pub_number, link,))
                    mydb.commit()
                    i += 1
                    print(f'{pub_number} articles appended into {link}')
                    #time.sleep(random.randint(3,8))
                    #pdb.set_trace()
                    break

        """
        sql = 'UPDATE profiles SET pub_number = 0, pub_scraped = 1 WHERE link = %s'
        cursor.execute(sql, (link,))
        mydb.commit()
        i += 1
        print('no publications')
        #time.sleep(random.randint(3,8))
        """
    else:
        sql = 'UPDATE profiles SET public_profile = 0 WHERE link = %s'
        cursor.execute(sql, (link,))
        mydb.commit()
        print('not public')
        #time.sleep(random.randint(1,3))
        i += 1


