# TODO: next riddle
import os
import json
from tqdm import tqdm
from utils import extract_wahlperiode, extract_sitzungsnummer


with open("raw_data/topics.json", "r") as f:
    topics = json.load(f)

def extract_keywords_topic(topic_name: str, keywords_file: str) -> None:
    topic_begriffe = topics[topic_name]
    topic_ausschluss_begriffe = []
    if isinstance(topic_begriffe, dict):
        topic_ausschluss_begriffe = topic_begriffe.get("ausschluss_begriffe", [])
        topic_begriffe = topic_begriffe.get("begriffe", [])
    print(topic_begriffe, topic_ausschluss_begriffe)
    with open(keywords_file) as f:
        data: dict = json.load(f)
    with open(f"data/topic_keywords_stemmed/{topic_name}_Daten.csv", "w+") as f:
        f.write("")
    write_data = {}
    for key in data.keys():
        keywords_dict: dict = data[key]
        for i in list(keywords_dict):
            for a in topic_ausschluss_begriffe:
                if a in i:
                    keywords_dict.pop(i)
        for item in keywords_dict:
            for begriff in topic_begriffe:
                if begriff in str(item):
                    wahlperiode = extract_wahlperiode(key)
                    if wahlperiode not in write_data: write_data[wahlperiode] = {}
                    sitzungsnummer = extract_sitzungsnummer(key)
                    if sitzungsnummer not in write_data[wahlperiode]: write_data[wahlperiode][sitzungsnummer] = {}
                    write_data[wahlperiode][sitzungsnummer][item] = keywords_dict[item]
                    with open(f"data/topic_keywords_stemmed/{topic_name}_Daten.csv", "a") as g:
                        g.write(f"{wahlperiode}_{sitzungsnummer}, {item} {keywords_dict[item]}\n")
    write_data = dict(sorted(write_data.items(), key=lambda x: int(x[0])))
    write_data = {k: dict(sorted(v.items(), key=lambda x: int(x[0]))) for k, v in write_data.items()}
    with open(f"data/topic_keywords_stemmed/{topic_name}_Daten.json", "w+") as f:
        json.dump(write_data, f, indent=4)


def extract_keywords_all() -> None:
    os.makedirs("data/topic_keywords_stemmed", exist_ok=True)
    for topic in tqdm(topics):
        extract_keywords_topic(topic, "data/keywords_wahlperiode/keywords_stemmed_100.json")


if __name__ == "__main__":
    extract_keywords_all()