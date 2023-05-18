import os
import json
from tqdm import tqdm
from utils import extract_wahlperiode, extract_sitzungsnummer


topics = {
    "klima": ["klima", "umweltkatastroph", "emission", "erneuerbar", "energiewende", "co2", "kohlenstoffdioxid", "methan", "treibhausgase"],
    "klimaschutz": ["klimaschutz"],
    "klima_kohle": ["braunkohle"],
    "wissenschaft": ["wissenschaft", "forschung", "hochschule", "universitaet"],
    "migration": ["fluechtl", "migration", "asyl", "schutzsuch", "abschieb"],
    "digitalisierung": ["digitaliserung", "computer", "internet", "datensicherheit"],
    "extremismus": ["rechtsextrem"],
    "corona": ["corona", "virus", "pandemie", "fallzahlen"],
    "bildung": {
        "begriffe": ["bildung", "pisa", "gymnasium", "mittelschul", "lehrer", "schueler", "lehrkraft"],
        "ausschluss_begriffe": ["ausbildung", "berufsbildung"],
    },
    "inklusion": {
        "begriffe": ["inklusion", "behinderung", "beeintraechtigung", "teilhab", "brk", "behindertenrechtskonvention"],
        "ausschluss_begriffe": ["brkg"],
    },
    "kommunales": ["miete", "sozialwohnungen"],
}



def extract_keywords_topic(topic_name: str, keywords_file: str) -> None:
    topic_begriffe = topics[topic_name]
    topic_ausschluss_begriffe = []
    if isinstance(topic_begriffe, dict):
        topic_ausschluss_begriffe = topic_begriffe.get("ausschluss_begriffe", [])
        topic_begriffe = topic_begriffe.get("begriffe", [])
        
    with open(keywords_file) as f:
        data = json.load(f)
    with open(f"data/topic_keywords_stemmed/{topic_name}_Daten.csv", "w+") as f:
        f.write("")
    for key in data.keys():
        keywords_dict = data[key]
        for i in list(keywords_dict):
            for a in topic_ausschluss_begriffe:
                if a in i:
                    keywords_dict.pop(i)
        for item in keywords_dict:
            for begriff in topic_begriffe:
                if begriff in str(item):
                    wahlperiode = extract_wahlperiode(key)
                    sitzungsnummer = extract_sitzungsnummer(key)
                    with open(f"data/topic_keywords_stemmed/{topic_name}_Daten.csv", "a") as g:
                        g.write(f"{wahlperiode}_{sitzungsnummer}, {item} {keywords_dict[item]}\n")


def extract_keywords_all() -> None:
    os.makedirs("data/topic_keywords_stemmed", exist_ok=True)
    for topic in tqdm(topics):
        extract_keywords_topic(topic, "data/keywords_wahlperiode/keywords_stemmed_100.json")


if __name__ == "__main__":
    extract_keywords_all()