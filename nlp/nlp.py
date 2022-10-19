from researchgate_scraping.db_functions import DbAuth

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
path = r'../datasets/arxiv-metadata-oai-snapshot.json'

# dict_keys(['id', 'submitter', 'authors', 'title', 'comments', 'journal-ref',
# 'doi', 'report-no', 'categories', 'license', 'abstract', 'versions', 'update_date', 'authors_parsed'])

topics = {
    'physics': 'astro-ph,cond-mat,gr-qc,hep-ex,hep-lat,hep-ph,hep-th,math-ph,nlin,nucl-ex,nucl-th,physics,quant-ph',
    'biology': 'q-bio',
    'math': 'math,stat',
    'economics': 'econ,q-fin',
    'cs': 'CoRR'
}
