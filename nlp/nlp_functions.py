import json
from db_functions import DbAuth

cursor, mydb = DbAuth()

def AppendTrainingPubs(path, table_number):
    # Appends pubs from json file to db

    with open(path, 'r') as f:
            for line in f:
                data = json.loads(line)
                id = data['id']
                title = data['title']
                category = data['categories']
                sql = f'INSERT INTO training_pubs{table_number} VALUES (%s, %s, %s)'
                cursor.execute(sql, (id, category, title,))
                mydb.commit()


def CategoryScores(topics, category_list):
    # adds scores to the categories and returns the score

    score = {
        'physics': 0,
        'biology': 0,
        'math': 0,
        'economics': 0,
        'cs': 0,
        'unknown': 0
    }

    items = topics.items()

    for sub_category in category_list:
        head, sep, tail = sub_category.partition('.') # splits on the . where the head is the leading word
        for item in items:
            if head in item[1]:
                score[item[0]] += 1
    if max(score.values()) > 0: # if any value is above zero
        return score
    else: # if there is no value above zero, the category will be unknown
        score['unknown'] += 1
        return score

def GetKey(val, dict):
    keys = []
    for key, value in dict.items():
        if val == value:
            keys.append(key)
    return keys


