from functions import *
import pdb
from selenium import webdriver
from selenium.webdriver.common.by import By
import regex as re


cursor, mydb = DbAuth()
sql = 'SELECT link FROM profiles WHERE pub_scraped = 0'
cursor.execute(sql)
profile_links = cursor.fetchall()
Login() # Dont login, all publications are visible
i = 0
for link in profile_links:
    link = link[0]
    research_link = link + '/research'
    driver.get(research_link)
    IsPublic()
    driver.find_element(By.CLASS_NAME, 'nova-legacy-c-nav__item')
    number_articles = driver.find_element(By.CLASS_NAME, 'is-selected')  # finds article number
    number_articles = re.findall('[0-9]+', number_articles.text)
    if bool(number_articles) == True:
        pub_number, pub_names, pub_links = GetPublications(number_articles=number_articles)
        sql = "UPDATE profiles SET pub_titles = %s, pub_links = %s, pub_number = %s, pub_scraped = 1 WHERE link = %s"
        cursor.execute(sql, (pub_names, pub_links, pub_number, link,))
        mydb.commit()
        i += 1
        print(f'{pub_number} articles appended into {link}\n iteration {i}')
    else:
        pass
