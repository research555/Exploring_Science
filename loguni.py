def AppendUniList(country):

    import pandas as pd
    from functions import db_auth, ResearchGateLinkGenerator
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


