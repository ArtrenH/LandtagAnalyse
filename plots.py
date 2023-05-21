import os
import json
from tqdm import tqdm
from bokeh.plotting import figure, show
import matplotlib.pyplot as plt

plt.style.use("Solarize_Light2")

def gather_period_lengths() -> list[int]:
    all_files = os.listdir("data/cleaned_content")
    return [0] + [len([elem for elem in all_files if elem.split("_")[2] == str(i)]) for i in range(1, 7+1)]

def gather_topic_data(topic: str):
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
    return periods, scores
    

def plot_topic(topic: str) -> None:
    plt.clf()
    os.makedirs("data/plots", exist_ok=True)
    plt.title(f"Wort-Cluster-Score pro Sitzung für Thema {topic}")
    plt.ylabel(f"tf-idf-score sum per sitzung")
    plt.xlabel("Wahlperiode")
    plt.bar(*gather_topic_data(topic))
    plt.xlim([0, 8])
    plt.tight_layout()
    plt.savefig(f"data/plots/{topic}.png", dpi=500)

def bokeh_plot(topic: str) -> None:
    p = figure(title=f"Analye der Scores für Wortfeld {topic}", x_axis_label="Wahlperiode", y_axis_label="tf-idf-score Summe pro Sitzung")
    periods, scores = gather_topic_data(topic)
    p.vbar(x=periods, top=scores, legend_label="tf-idf-scores", width=0.5, bottom=0, color="violet")
    show(p)

def plot_all_topics() -> None:
    with open("raw_data/topics.json", "r") as f:
        topics = json.load(f).keys()

    for topic in tqdm(topics):
        plot_topic(topic)

if __name__ == "__main__":
    plot_all_topics()
