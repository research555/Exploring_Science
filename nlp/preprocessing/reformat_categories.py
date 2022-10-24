import pdb

from db_functions import DbAuth
from preprocessing_functions import *

"""

The test set is around 4 GB of a JSON file with classifications from kaggle. this causes memory issues, so perhaps
it is wiser to take every 1000 lines and turn it into a separate json for easier processing.

Decided to be lazy and just parse line by line

"""




cursor, mydb = DbAuth()
path = r'../../datasets/arxiv-metadata-oai-snapshot.json'

# dict_keys(['id', 'submitter', 'authors', 'title', 'comments', 'journal-ref',
# 'doi', 'report-no', 'categories', 'license', 'abstract', 'versions', 'update_date', 'authors_parsed'])

topics = {
    'physics': ['astro-ph', 'cond-mat', 'gr-qc', 'hep-ex', 'hep-lat','hep-ph','hep-th', 'math-ph', 'nlin','nucl-ex','nucl-th','physics', 'quant-ph'],
    'biology': ['q-bio'],
    'math': ['math', 'stat'],
    'economics': ['econ', 'q-fin'],
    'cs': ['CoRR', 'cs'],
    'unknown': ['unknown']
}

for table_number in range(19):
    sql = f'SELECT category, title FROM training_pubs{table_number} WHERE formatted_category IS NULL'
    cursor.execute(sql)
    cat_and_title = cursor.fetchall()
    i = 0
    print(table_number)
    for category, title in cat_and_title:
        number_entries = len(cat_and_title)
        category_list = category.split(' ')
        scores = CategoryScores(topics=topics, category_list=category_list)
        max_score = max(scores.values())
        max_keys = GetKey(max_score, scores)
        print(max_keys)
        if len(max_keys) == 1: # handle multiple ones later, for now do single topic journals
            for key in max_keys:
                sql = f"UPDATE training_pubs{table_number} SET formatted_category = %s WHERE title = %s "
                cursor.execute(sql, (key, title,))
                mydb.commit()
                print(f'added record number {i} out of {number_entries}')
                i += 1





