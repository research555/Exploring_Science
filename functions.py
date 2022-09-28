def login(driver, username, password):
    #Login to researchgate
    import os
    from dotenv import load_dotenv
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys

    load_dotenv()
    driver.get(os.getenv('RG_LOGIN'))
    driver.find_element(By.ID, 'input-login').send_keys(username)  # Fills username
    driver.find_element(By.ID, 'input-password').send_keys(password, Keys.ENTER)    # Enters password and logs in

def db_auth():
    # init database

    import os
    import mysql.connector
    from dotenv import load_dotenv
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

def ResearchGateLinkGenerator(name, researcher=False, just_uni=False):

    """
    Turns out that researchgate will correct underscored links, but not hyphenated ones. This means that some institutions
    that have hyphens can be written with underscores, but if you write one with underscores with hyphens it wont work.
    As confusing as that sounds, Thats why all links are underscored. The more you know..

    """

    underscore = name.replace(' ', '_')

    if just_uni == True:
        return underscore

    else:
        if researcher:
            link = f'https://www.researchgate.net/profile/{underscore}'
        if not researcher:
            link = f'https://www.researchgate.net/institution/{underscore}'

        # noinspection PyUnboundLocalVariable
        return link

def LogMemberNumber(driver, university):

    import regex
    from selenium.webdriver.common.by import By

    cursor, mydb = db_auth()
    heading = driver.find_elements(By.CLASS_NAME, 'nova-legacy-c-nav__item-label') # Finds labels
    try:
        for elements in heading:
            text = elements.text.lower()
            if 'members' in text:
                number_members = regex.findall(r'[0-9]', text) # Finds number of members. turns into list. handles comma
                number_members = int(''.join(number_members)) # turns into an int for db column
                sql = "INSERT INTO universities (institution, member_number) VALUES(%s, %s)"
                cursor.execute(sql, (university, number_members,))
                mydb.commit()
                return 1
    except Exception as e:
        return e  # handle exceptions


def AppendUniList(country):


    # note to self, remove special characters and apostrophes


    import pandas as pd
    import os
    from dotenv import load_dotenv
    import country_converter as coco

    load_dotenv()
    cursor, mydb = db_auth()
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

def LogProfiles(driver, university):
    from selenium import webdriver
    from selenium.webdriver.common.by import By

    cursor, mydb = db_auth()
    profile = driver.find_elements(By.CLASS_NAME, 'institution-members-list')

    for x in profile:
        try:
            link = x.find_element(By.CLASS_NAME, 'nova-legacy-e-link--theme-bare').get_attribute('href')
            sql = f'INSERT INTO profiles VALUES (%s, %s)'
            cursor.execute(sql, (university, link,))
            mydb.commit()


        except Exception as e:
            if e.__class__.__name__ == 'IntegrityError':
                pass
            else:
                return e

def LatinLetters(str):
    import string

    char_set = string.ascii_letters + "',._"
    return all([True if x in char_set else False for x in str])  #returns true if all letters are latin (a-z)

def GetPublications(profile):
    # get publications profile/name/research db testpub
    # spinner for profiles with research but need to scroll to see more

    from selenium import webdriver
    from selenium.webdriver.common.by import By
    import os
    from dotenv import load_dotenv
    import regex as re
    import time
    import math

    cursor, mydb = db_auth()
    username = os.getenv('RG_USER')
    password = os.getenv('RG_PASSWORD')
    driver = webdriver.Edge(executable_path='C:/Users/imran/PycharmProjects/Exploring_Science/Driver/msedgedriver.exe')
    login(driver=driver, username=username, password=password)
    pub_names = []
    pub_links = []
    research_link = profile + '/research'
    driver.get(research_link)
    driver.find_element(By.CLASS_NAME, 'nova-legacy-c-nav__item')
    number_articles = driver.find_element(By.CLASS_NAME, 'is-selected')  # finds article number
    number_articles = re.findall('[0-9]+', number_articles.text)
    if bool(number_articles) == True:
        # author has publications
        number_scrolls = math.ceil(int(number_articles[0]) / 10) + 3
        for i in range(number_scrolls):
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")  # scrolls to bottom
            time.sleep(1.5)
        pub_class = driver.find_elements(By.CLASS_NAME, 'nova-legacy-v-publication-item__title')
        for i in pub_class:
            pub_names.append(i.text)  # finds publication name NOTE, INCLUDE HREF
            pub_links.append(i.get_attribute('href'))

        pub_names = '%%%'.join(pub_names)
        pub_links = '&&&'.join(pub_links)
        sql = "UPDATE profiles SET pub_names = %s, pub_links = %s WHERE link = %s"
        cursor.execute(sql, (pub_names, pub_links, profile,))
        mydb.commit()

    else:
        # author has no publications
        pass
