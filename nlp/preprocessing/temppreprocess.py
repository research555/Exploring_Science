from db_functions import DbAuth

cursor, mydb = DbAuth()

sql = "SELECT pub_titles FROM profiles_cleanup"
cursor.execute(sql)
result = cursor.fetchall()
length = len(result)
i = 0
for title in result:
    if 'figure' in title[0].lower().split() and len(title[0].split()) <= 5:

        sql = 'INSERT INTO paper_or_not (not_paper) VALUE (%s)'
        cursor.execute(sql, (title[0],))
        mydb.commit()
        sql = 'DELETE FROM profiles_cleanup WHERE pub_titles = "%s"'
        cursor.execute(sql, (title[0],))
        mydb.commit()
        i += 1
        print(f'iteration {i}')
