import os
import json
from tqdm import tqdm
import matplotlib.pyplot as plt

plt.style.use("Solarize_Light2")

def gather_period_lengths():
    all_files = os.listdir("data/cleaned_content")
    return [0] + [len([elem for elem in all_files if elem.split("_")[2] == str(i)]) for i in range(1, 7+1)]

def plot_topic(topic: str):
    plt.clf()
    os.makedirs("data/plots", exist_ok=True)
    period_lengths = gather_period_lengths()
    with open(f"data/topic_keywords_stemmed/{topic}_Daten.json", "r") as f:
        data: dict = json.load(f)
    periods = []
    scores = []
    for period, period_data in data.items():
        periods.append(int(period))
        scores.append(
            sum([sum(elem.values()) for elem in period_data.values()])/period_lengths[int(period)]
        )
    plt.title(f"Wort-Cluster-Score pro Plenarsitzung für Thema {topic}")
    plt.ylabel(f"tf-idf-score sum per sitzung")
    plt.xlabel("Wahlperiode")
    plt.bar(periods, scores)
    plt.xlim([0, 8])
    plt.savefig(f"data/plots/{topic}.png", dpi=500)

with open("raw_data/topics.json", "r") as f:
    topics = json.load(f).keys()

for topic in tqdm(topics):
    plot_topic(topic)
