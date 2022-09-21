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



"""
STEPS

MAKE A LIST OF ALL UNIVERSITIES
1. OPEN AND LOG INTO RESEARCHGATE

2. NAVIAGTE TO INSTITUTIONS DIRECTORY


"""



username = os.getenv('RG_USER')
password = os.getenv('RG_PASSWORD')

driver = webdriver.Edge(executable_path='C:/Users/imran/PycharmProjects/Exploring_Science/Driver/msedgedriver.exe')

# # # # LOGIN TO Researchgate # # # #

#driver.get('https://www.linkedin.com')      #   Starts LinkedIn
#login(driver=driver, username=username, password=password)

# # # # Google and get links # # # #
driver.get('https://researchgate.net/login')
login(driver=driver, username=username, password=password)

driver.get(f'https://www.researchgate.net/institution/University-of-Northern-Iowa/members')
heading = driver.find_elements(By.CLASS_NAME, 'nova-legacy-c-nav__item-label')

cursor, mydb = db_auth()

for elements in heading:
    text = elements.text.lower()
    if 'members' in text:
        number_members = regex.findall(r'[0-9]', text)
        number_members = int(''.join(number_members))
        cursor.execute("INSERT INTO universities (institution, member_number) VALUES(%s, %s)", (number_members, ))
        mydb.commit()


#press next page

"""

FINDS LINKS, FUNCTIONAL

profile = driver.find_elements(By.CLASS_NAME,
                              'institution-members-list')
for x in profile:
    links = x.find_element(By.CLASS_NAME, 'nova-legacy-e-link--theme-bare').get_attribute('href')
    
    """





#for university in x['university']:
    #pass
    #link = ResearchGateLinkGenerator(name=university, researcher=False)


#search = driver.find_element(By.NAME, 'q').send_keys('site:linkedin.com/in/ AND "molecular biology"', Keys.ENTER)
"""
links = driver.find_elements(By.CSS_SELECTOR, 'div.g')

for link in links:
    url = link.find_element(By.TAG_NAME, 'a').get_attribute('href')
    print(url)
    #if url is True:
        #print(url)
        #sql = 'INSERT INTO researcher_details (url) VALUE (%s)'
        #cursor.execute(sql, (url,))
    #else:
        #print(url)

results = cursor.execute('SELECT * FROM researcher_url')
for result in results:
    print(result)



#links = driver.find_element(By.TAG_NAME, 'a').get_attribute('href')
#print((links))


# scrape one link put into database
# scrape xp and education into database
# repeat 1 million times
# make graphical interface
"""