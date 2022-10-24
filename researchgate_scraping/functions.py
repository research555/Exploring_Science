import pdb

import regex as re
import math
import string
import pandas as pd
import country_converter as coco
import mysql.connector
import os
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium import webdriver
import random



# turn into class

load_dotenv()
driver = webdriver.Edge(executable_path=os.getenv('EDGE_WEBDRIVER_PATH'))


def Login():
    #Login to researchgate

    load_dotenv()
    username = os.getenv('RG_USER')
    password = os.getenv('RG_PASSWORD')
    driver.get(os.getenv('RG_LOGIN'))
    time.sleep(3)
    accept = driver.find_element(By.CLASS_NAME, 'css-1u05hh5')
    accept.click()  # Accepts cookies
    time.sleep(1)
    driver.find_element(By.ID, 'input-login').send_keys(username)  # Fills username
    driver.find_element(By.ID, 'input-password').send_keys(password, Keys.ENTER)    # Enters password and logs in


def DbAuth():
    # init database

    load_dotenv()

    # # # # Define auth details # # # #

    DB_HOSTNAME = os.getenv('DB_HOSTNAME')
    DB_USERNAME = os.getenv('DB_USERNAME')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_DATABASE = os.getenv('DB_DATABASE')

    # # # # Connect to MySQL Database# # # #

    mydb = mysql.connector.connect(
        host=DB_HOSTNAME,
        user=DB_USERNAME,
        password=DB_PASSWORD,
        database=DB_DATABASE
    )

    cursor = mydb.cursor(buffered=True)  # Name the cursor something simple for easier use

    return cursor, mydb

cursor, mydb = DbAuth()


def ResearchGateLinkGenerator(name, researcher=False, just_uni=False):

    """
    Turns out that researchgate will correct underscored links, but not hyphenated ones. This means that some institutions
    that have hyphens can be written with underscores, but if you write one with underscores with hyphens it wont work.
    As confusing as that sounds, Thats why all links are underscored. The more you know..

    """

    underscore = name.replace(' ', '_')

    if just_uni is True:
        return underscore

    else:
        if researcher:
            link = f'https://www.researchgate.net/profile/{underscore}'
            return link
        if not researcher:
            link = f'https://www.researchgate.net/institution/{underscore}'
            return link


def LogMemberNumber(university):


    cursor, mydb = DbAuth()
    heading = driver.find_elements(By.CLASS_NAME, 'nova-legacy-c-nav__item-label') # Finds labels
    try:
        for elements in heading:
            text = elements.text.lower()
            if 'member' in text:
                number_members = re.findall(r'[0-9]', text) # Finds number of members. turns into list. handles comma
                number_members = int(''.join(number_members)) # turns into an int for db column
                sql = "INSERT INTO universities (institution, member_number) VALUES(%s, %s)"
                cursor.execute(sql, (university, number_members,))
                mydb.commit()
                return 1
    except Exception as e:
        return e  # handle exceptions


def AppendUniList(country):

    # note to self, remove special characters and apostrophes



    load_dotenv()
    cursor, mydb = DbAuth()
    full_unis = pd.read_csv(filepath_or_buffer=os.getenv('UNI_CSV_PATH'))
    iso2_country = coco.convert(names=country, to='ISO2')

    try:
        country_specific_uni = full_unis.loc[full_unis['iso2'] == f'{iso2_country}']
        for i in country_specific_uni['university']:
            ascii = LatinLetters(i)
            if ascii is True:
                formatted_university = ResearchGateLinkGenerator(just_uni=True, name=i)
                link = ResearchGateLinkGenerator(name=i)
                sql = "INSERT INTO universities (institution, link, iso2) VALUE (%s, %s, %s)"
                cursor.execute(sql, (formatted_university, link, iso2_country,))
                mydb.commit()
                return True
            else:
                pass # handle exception if it is not ascii
    except Exception as e:
        return e


def LatinLetters(str):
    # returns true if all letters are latin (a-z)

    char_set = string.ascii_letters + ' '
    return all([True if x in char_set else False for x in str])

def GetPublications(public: bool, number_articles, profile_link=None):
    # get publications profile/name/research db testpub
    # spinner for profiles with research but need to scroll to see more
    # FIXME: Only appends 100 publications maximum for some reason

    pub_names = []
    pub_links = []

    if public is True:
        if int(number_articles[0]) <= 100:
            pub_class = driver.find_elements(By.CLASS_NAME, 'nova-legacy-v-publication-item__title')
            for publication in pub_class:
                pub_link = publication.find_element(By.CLASS_NAME, 'nova-legacy-e-link')
                link = pub_link.get_attribute('href')
                pub_names.append(publication.text)  # finds publication name NOTE, INCLUDE HREF
                pub_links.append(link)
        else:
            #pdb.set_trace()
            num_pages = math.ceil(int(number_articles[0]) / 100)
            for i in range(1, num_pages + 1):
                driver.get(f'{profile_link}/{i}')
                pub_class = driver.find_elements(By.CLASS_NAME, 'nova-legacy-v-publication-item__title')
                for publication in pub_class:  # Include href for good measure
                    pub_link = publication.find_element(By.CLASS_NAME, 'nova-legacy-e-link')
                    link = pub_link.get_attribute('href')
                    pub_names.append(publication.text)
                    pub_links.append(link)
            #driver.get(profile_link)
        pub_names_str = '%%%'.join(pub_names)
        pub_links_str = '&&&'.join(pub_links)

        return len(pub_links), pub_names_str, pub_links_str

    else:
        number_scrolls = math.ceil(int(number_articles[0]) / 10) + 3
        for i in range(number_scrolls):
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")  # scrolls to bottom
            time.sleep(1.5)
        pub_class = driver.find_elements(By.CLASS_NAME, 'nova-legacy-v-publication-item__title')
        for publication in pub_class:
            pub_link = publication.find_element(By.CLASS_NAME, 'nova-legacy-e-link')
            link = pub_link.get_attribute('href')
            pub_names.append(publication.text)  # finds publication name NOTE, INCLUDE HREF
            pub_links.append(link)
        pub_names_str = '%%%'.join(pub_names)
        pub_links_str = '&&&'.join(pub_links)

        return len(pub_links), pub_names_str, pub_links_str

def GetPageAndMemberNumber(login: bool, university):

    heading = driver.find_elements(By.CLASS_NAME, 'nova-legacy-c-nav__item-label')  # finds navbar with member number
    for elements in heading:
        text = elements.text.lower()
        if 'members' in text:
            number_members = re.findall(r'[0-9]', text)
            number_members = int(''.join(number_members))  # remove commas
            sql = 'UPDATE universities SET member_number = %s WHERE institution = %s'
            cursor.execute(sql, (number_members, university,))
            mydb.commit()
            num_pages = math.ceil(number_members/10) if login else math.ceil(number_members/100) # number members depends on login status

            return num_pages, number_members

def LogAllProfiles(num_pages, university, current_url):
    # # # # LOGS ALL PROFILES OF AN INSTITUTION # # # #

    if '/members' in current_url:  #There is dedicated members page
        for pages in range(1, num_pages+1):
            time.sleep(random.randint(1, 3)) # avoid captcha
            driver.get(f'https://www.researchgate.net/institution/{university}/members/{pages}')
            profiles = driver.find_elements(By.CLASS_NAME, 'institution-members-list')
            try:
                for profile in profiles:
                    link = profile.find_element(By.CLASS_NAME, 'nova-legacy-e-link--theme-bare').get_attribute(
                        'href')  # gets profile link
                    sql = 'INSERT INTO profiles (institution, link) VALUES (%s, %s)'
                    cursor.execute(sql, (university, link,))
                    mydb.commit()
            except Exception as e:
                if e.__class__.__name__ == 'IntegrityError': # ignores duplicates
                    pass
                else:
                    return e

    else: #There is no dedicated members page
        cards = driver.find_elements(By.CLASS_NAME, 'nova-legacy-c-card__header')
        for card in cards:
            if 'member' in card.text:
                profiles = driver.find_elements(By.CLASS_NAME, 'nova-legacy-v-person-list-item__stack-item')
                for profile in profiles:
                    name_div = profile.find_element(By.CLASS_NAME, 'nova-legacy-e-link')
                    sql = "INSERT INTO profiles (institution, link) VALUES (%s, %s)"
                    cursor.execute(sql, (university, name_div.get_attribute('href'),))
                    mydb.commit()




def IsPublic(link):
    from selenium.webdriver.common.by import By

    first_line = driver.find_element(By.CLASS_NAME, 'nova-legacy-e-text')
    if first_line.text == 'Browse researchers alphabetically by name':
        sql = "UPDATE profiles SET public_profile = 0 WHERE link = %s"
        cursor.execute(sql, (link,))
        mydb.commit()
        return False
    else:
        sql = "UPDATE profiles SET public_profile = 1 WHERE link = %s"
        cursor.execute(sql, (link,))
        mydb.commit()
        return True


def HasPublications(public: bool):

    if public is True:
        sections = driver.find_elements(By.CLASS_NAME, 'nova-legacy-c-card__header')
        for section in sections:
            if 'publication' in section.text.lower():
                number_articles = re.findall('[0-9]+', section.text)
                return number_articles
            else:
                return False
    else:
        driver.find_element(By.CLASS_NAME, 'nova-legacy-c-nav__item')
        number_articles = driver.find_element(By.CLASS_NAME, 'is-selected')  # finds article number
        number_articles = re.findall('[0-9]+', number_articles.text)
        return number_articles

def AppendAllUnis(csv_path):

    cursor, mydb = DbAuth()
    load_dotenv()

    csv = pd.read_csv(filepath_or_buffer=csv_path)
    i = 0
    for i in range(len(csv.university)):
        row = csv.iloc[i]
        latin = LatinLetters(row.university)
        institution = ResearchGateLinkGenerator(name=row.university, just_uni=True)
        link = ResearchGateLinkGenerator(name=institution)
        iso2 = row.iso2
        if latin:
            try:
                sql = "INSERT INTO universities(institution, iso2, link) VALUES (%s, %s, %s)"
                cursor.execute(sql, (institution, iso2, link,))
                mydb.commit()
                i += 1
            except Exception as e:
                # duplicate entry: handle later but not important
                i += 1
                pass
        else:
            i +=1
            pass


def UpdateLink(current_url, members_link):

    link_split = current_url.split('/')
    institution_index = link_split.index('institution')
    value = link_split[institution_index + 1]  # in case there is '/something' else after the uni name
    if '-' in value:
        sql = 'UPDATE universities SET institution = %s, link = %s, members_link = %s, hyphenated = 1 WHERE link = %s '
        cursor.execute(sql, (value, current_url, members_link, current_url,))
        mydb.commit()
    else:
        pass

# # # # SQL FUNCTIONS # # # #

def SetSuccess(success: int, university):
    sql = 'UPDATE universities SET success = %s WHERE institution = %s'
    cursor.execute(sql, (success, university,))
    mydb.commit()
def SetTried(tried: int, university):
    sql = 'UPDATE universities SET tried = %s WHERE institution = %s'
    cursor.execute(sql, (tried, university,))
    mydb.commit()


if __name__ == '__main__':
    pass
