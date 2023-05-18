import os
import json
import re
from tqdm import tqdm
import nltk
from nltk.corpus import stopwords
import time

def init_nltk():
    nltk.download('stopwords')
    nltk.download('punkt')

# extraction of actual content
class JsonHandler():
    def __init__(self, filepath):
        self.filepath = filepath
        self.name = self.filepath.split("/")[-1]

    def get_content(self) -> str:
        with open(self.filepath) as f:
            return json.load(f)["content"]

    def extract_wahlperiode_json(self) -> str:
        return self.name.split("_")[0]
    
    def extract_sitzungsnummer_json(self) -> str:
        return self.name.split("_")[2]

def extract_contents():
    os.makedirs("raw_data/content", exist_ok=True)
    for wahlperiode in [f"wahlperiode-{i}" for i in range(1, 7+1)]:
        for file in os.listdir(f"raw_data/json/{wahlperiode}"):
            handler = JsonHandler(f"raw_data/json/{wahlperiode}/{file}")
            with open(f"raw_data/content/inhalt_wahlperiode_{handler.extract_wahlperiode_json()}_{handler.extract_sitzungsnummer_json()}_.txt", "w+") as f:
                f.write(handler.get_content())


# DATA CLEANING -> remove stopwords and punctuation

def clean_data(resumable=True) -> None:
    os.makedirs("data/cleaned_content", exist_ok=True)
    stopwords_liste = ["staatsregierung", "landtag", "fuer", "koennen", "koennte", "ueber", "waehrend", "wuerde", "wuerden", "herr", "frau", "wer", "ueber", "heute", "ja", "nein", "beifall", "praesident", "vizepraesident", "linke", "gruene", "fdp", "cdu", "spd", "pds", "afd", "linksfraktion", "buendnisgruenen", "buendnisgruene", "damen", "herren", "bitte", "schon", "prof", "dr", "staatsminister", "januar", "februar", "maerz", "april", "mai", "juni", "juli", "august", "september", "oktober", "november", "dezember", "fraktion", "antrag", "gesetz", "drucksache"]

    for element in tqdm(os.listdir("raw_data/content")):
        if resumable and os.path.exists(f"data/cleaned_content/{element}"):
            continue
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
    print("initialising nltk data ...")
    init_nltk()
    print("extracting contents...")
    extract_contents()
    print("cleaning data...")
    clean_data()

