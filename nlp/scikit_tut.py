from sklearn.datasets import fetch_20newsgroups

categories = ['alt.atheism', 'soc.religion', 'comp.graphics', 'sci.med']
twenty_train = fetch_20newsgroups(subset='train', categories=categories, shuffle=True, random_state=42)

print(twenty_train.target_names)