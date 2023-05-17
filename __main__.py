from utils import extract_contents
from preparation import clean_data
from stemming import stem_all


# extract contents from json files
print("extracting contents ...")
extract_contents()

# unterbrechungen?


# prepare texts (remove stopwords etc.)
print("cleaning up text data ...")
clean_data()

# stem the words
print("stemming words")
stem_all()

# keyword extraction

