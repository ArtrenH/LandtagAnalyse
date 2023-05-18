import os
import re
from tqdm import tqdm
from nltk.corpus import stopwords
import time

# DATA CLEANING -> remove stopwords and punctuation

def clean_data() -> None:
    os.makedirs("data/cleaned_content", exist_ok=True)
    stopwords_liste = ["staatsregierung", "landtag", "fuer", "koennen", "koennte", "ueber", "waehrend", "wuerde", "wuerden", "herr", "frau", "wer", "ueber", "heute", "ja", "nein", "beifall", "praesident", "vizepraesident", "linke", "gruene", "fdp", "cdu", "spd", "pds", "afd", "linksfraktion", "buendnisgruenen", "buendnisgruene", "damen", "herren", "bitte", "schon", "prof", "dr", "staatsminister", "januar", "februar", "maerz", "april", "mai", "juni", "juli", "august", "september", "oktober", "november", "dezember", "fraktion", "antrag", "gesetz", "drucksache"]

    for element in tqdm(os.listdir("raw_data/content")):
        with open(f"raw_data/content/{element}", 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read()
        t = time.perf_counter()
        content = re.sub('ä', 'ae', content)
        content = re.sub('ö', 'oe', content)
        content = re.sub('ü', 'ue', content)
        content = re.sub("[^A-Za-z0-9]+", " ", content)
        content = content.lower().split()
        content = [word for word in content if not word.isdigit()]
        # next 2 lines are sloooow
        content = [word for word in content if word not in stopwords_liste]
        content = [word for word in content if word not in stopwords.words('german')]
        content = ' '.join(content)
        with open(f"data/cleaned_content/{element}", "w+") as f:
            f.write(content)


if __name__ == "__main__":
    clean_data()

