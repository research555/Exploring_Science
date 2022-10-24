from db_functions import DbAuth

def clean_profiles():
    cursor, mydb = DbAuth()

    sql = 'SELECT link, pub_titles FROM profiles WHERE pub_number >  1'
    cursor.execute(sql)
    result = cursor.fetchall()
    i = 0
    for link, titles in result:
        i += 1
        titles = titles.split('%%%')
        for title in titles:
            print(link, title)
            sql = 'INSERT INTO profiles_cleanup VALUES (%s, %s)'
            cursor.execute(sql, (link, title,))
            mydb.commit()
            print(f'iteration {i} out of {len(result)}')
    return True


cursor, mydb = DbAuth()

sql = "SELECT pub_titles FROM profiles_cleanup"
cursor.execute(sql)
result = cursor.fetchall()
length = len(result)
i = 0
for title in result:
    if 'supplemental' in title[0].lower().split() and len(title[0].split()) <= 5:
        print(title)
        sql = 'INSERT INTO paper_or_not (not_paper) VALUE (%s)'
        cursor.execute(sql, (title[0],))
        mydb.commit()
        sql = 'DELETE FROM profiles_cleanup WHERE pub_titles = "%s"'
        cursor.execute(sql, (title[0],))
        mydb.commit()
        i += 1
        print(f'iteration {i} out of {length}')

