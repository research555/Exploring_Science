import json
from researchgate_scraping.db_functions import DbAuth

cursor, mydb = DbAuth()

def AppendTrainingPubs(path):
    with open(path, 'r') as f:
            i = 0
            for line in f:
                data = json.loads(line)
                id = data['id']
                title = data['title']
                category = data['categories']
                sql = 'INSERT INTO training_pubs VALUES (%s, %s, %s)'
                cursor.execute(sql, (id, category, title,))
                mydb.commit()
                i += 1
                print(f'iteration {i}')

