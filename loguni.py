import pandas as pd
import os
from dotenv import load_dotenv
import country_converter as coco
from functions import ResearchGateLinkGenerator, db_auth

load_dotenv()
cursor, mydb = db_auth()
full_unis = pd.read_csv(filepath_or_buffer=os.getenv('UNI_CSV_PATH'))
iso2_country = coco.convert(names=country, to='ISO2')

try:
    country_specific_uni = full_unis.loc[full_unis['iso2'] == f'{iso2_country}']
    for i in country_specific_uni['university']:
        formatted_university = ResearchGateLinkGenerator(just_uni=True, name=i)
        link = ResearchGateLinkGenerator(name=i)
        sql = "INSERT INTO universities (institution, link, iso2) VALUE (%s, %s, %s)"
        cursor.execute(sql, (formatted_university, link, iso2_country,))
        mydb.commit()
except Exception as e:
    print(e)