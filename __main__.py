from preparation import extract_contents, clean_data
from stemming import stem_all
from keyword_extraction import extract_keywords
from keywords_dokumente_auswertung import extract_keywords_all
from plots import plot_all_topics

step_data = [
    { # preparation.py
        "desc": "extracting contents",
        "function": extract_contents
    }, { # preparation.py
        "desc": "cleaning up text data",
        "function": clean_data
    },
    # unterbrechungen?
    { # stemming.py
        "desc": "stemming words",
        "function": stem_all
    }, { # keyword_extraction.py
        "desc": "extracting keywords",
        "function": extract_keywords
    }, { # keywords_dokumente_auswertung.py
        "desc": "collecting topics",
        "function": extract_keywords_all
    }, { # plots.py
        "desc": "plotting topics",
        "function": plot_all_topics
    }
]

def execute_all():
    for step in step_data:
        print(f"{step['desc']}...")
        step["function"]()

if __name__ == "__main__":
    execute_all()