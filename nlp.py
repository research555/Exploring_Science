import nltk
import json
import os
import sys
from db_functions import DbAuth

"""

The test set is around 2 GB of a JSON file with classifications from kaggle. this causes memory issues, so perhaps
it is wiser to take every 1000 lines and turn it into a separate json for easier processing.

Decided to be lazy and just parse line by line

"""


def get_key(val, dict):
    for key, value in dict.items():
        if val == value:
            return key

    return "key doesn't exist"



cursor, mydb = DbAuth()
path = r'datasets/arxiv-metadata-oai-snapshot.json'

# dict_keys(['id', 'submitter', 'authors', 'title', 'comments', 'journal-ref',
# 'doi', 'report-no', 'categories', 'license', 'abstract', 'versions', 'update_date', 'authors_parsed'])

topics = {
    'physics': 'astro-ph,cond-mat,gr-qc,hep-ex,hep-lat,hep-ph,hep-th,math-ph,nlin,nucl-ex,nucl-th,physics,quant-ph',
    'biology': 'q-bio',
    'math': 'math,stat',
    'economics': 'econ,q-fin',
    'cs': 'CoRR'
}

#x = 'astro-ph,cond-mat,gr-qc,hep-ex,hep-lat,hep-ph,hep-th,math-ph,nlin,nucl-ex,nucl-th,physics,quant-ph'
y = 'physics'

if y in topics['physics']:
    print(y)


with open(path, 'r') as f:
        i = 0
        for line in f:
            data = json.loads(line)
            id = data['id']
            title = data['title']
            category = data['categories']
            """
            if category in topics['physics']:
                topic = 'physics'
            elif category in topics['biology']:
                topic = 'biology'
            elif category in topics['math']:
                topic = 'math'
            elif category in topics['economics']:
                topic = 'economics'
            elif category in topics['cs']:
                topic = 'cs'
            else:
                topic = 'unknown'
            """
            sql = 'INSERT INTO training_pubs VALUES (%s, %s, %s)'
            cursor.execute(sql, (id, category, title))
            mydb.commit()
            i += 1
            print(f'iteration {i}')
