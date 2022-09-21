def login(driver, username, password):
    #Login to researchgate

    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys

    #driver.find_element(By.CLASS_NAME, 'nav__button-secondary').click()  # Clicks on Login
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

    cursor = mydb.cursor()  # Name the cursor something simple for easier use

    return cursor, mydb

def ResearchGateLinkGenerator(name, researcher=False, just_uni=False):

    """
    Turns out that researchgate will correct underscored links, but not hyphenated ones. This means that some institutions
    that have hyphens can be written with underscores, but if you write one with underscores with hyphens it wont work.
    As confusing as that sounds, Thats why all links are underscored. The more you know..

    """

    if just_uni == True:
        underscore = name.replace(' ', '_')
        return underscore

    if just_uni == False:
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
            formatted_university = ResearchGateLinkGenerator(just_uni=True, name=i)
            sql = "INSERT INTO universities (institution) VALUE (%s)"
            cursor.execute(sql, (formatted_university,))
            mydb.commit()
            return 1
    except Exception as e:
        return 0