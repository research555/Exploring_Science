from functions import ResearchGateLinkGenerator, LatinLetters, DbAuth
import geopy
import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv
import country_converter as coco

load_dotenv()

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