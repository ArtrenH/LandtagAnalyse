import json
import os
from tqdm import tqdm
from utils import sort_coo, extract_top_from_vector

from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer


def sort_coo(coo_matrix):
    tuples = zip(coo_matrix.col, coo_matrix.data)
    return sorted(tuples, key=lambda x: (x[1], x[0]), reverse = True)


content = {}
files = os.listdir("data/cleaned_content_stemmed")
for file in files:
    with open(f"data/cleaned_content_stemmed/{file}", 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()
    content[file] = text


        
keywords_dict = {}
cv = CountVectorizer(max_df=0.85)
word_count_vector = cv.fit_transform(content.values())
feature_names = cv.get_feature_names_out()

tfidf_transformer = TfidfTransformer(smooth_idf=True,use_idf=True)
tfidf_transformer.fit(word_count_vector)

for key in tqdm(content):
    doc = content[key]
    # generate tf-idf for the given document
    tf_idf_vector = tfidf_transformer.transform(cv.transform([doc]))
    # sort the tf-idf vectors by descending order of scores
    sorted_items = sort_coo(tf_idf_vector.tocoo())
    # extract only the top n; n here is 10
    keywords_dict[key] = extract_top_from_vector(feature_names, sorted_items, 100)
    
with open("data/keywords_wahlperiode/keywords_stemmed_100.json", "w") as h:
    json.dump(keywords_dict, h, indent = 4)