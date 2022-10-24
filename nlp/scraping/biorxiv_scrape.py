import random
import time
from db_functions import DbAuth
from selenium import webdriver
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import os

load_dotenv()
category = 'biology'
cursor, mydb = DbAuth()
driver = webdriver.Edge(executable_path=os.getenv('EDGE_WEBDRIVER_PATH'))

for i in range(1500, 10500): #gets 100k papers
    page_number = i
    biorxiv_pubs_link = f'https://www.biorxiv.org/content/early/recent?page={page_number}'
    driver.get(biorxiv_pubs_link)
    main_wrapper = driver.find_element(By.CLASS_NAME, 'main-content-wrapper')
    high_wires = main_wrapper.find_element(By.CLASS_NAME, 'highwire-list')
    titles = high_wires.find_elements(By.CLASS_NAME, 'highwire-cite-title')
    title_text = list(set(title.text for title in titles)) # set removes duplicates and outer list reforms the list
    for title in title_text:
        try:
            sql = 'INSERT INTO bio_training_pubs (category, title) VALUES (%s, %s)'
            cursor.execute(sql, (category, title,))
            mydb.commit()
        except Exception as e:
            pass
    print(f'appended page {i} out of 10500')
    time.sleep(random.randint(1, 3))




