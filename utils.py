import json


class JsonHandler():
    def __init__(self, filepath):
        self.filepath = filepath
        self.name = self.filepath.split("/")[-1]

    def get_content(self) -> str:
        with open(self.filename) as f:
            return json.load(f)["content"]

    def extract_wahlperiode_json(self) -> str:
        return self.name.split("_")[0]
    
    def extract_sitzungsnummer_json(self) -> str:
        return self.name.split("_")[2]

def extract_sitzungsnummer(name: str) -> str:
    return name.split("_")[3]

def extract_wahlperiode(name: str) -> str:
    return name.split("_")[2]

def extract_wahlperiode_folder(name: str) -> str:
    return name.split("-")[1]


def extract_sprecherdaten_name(filename: str) -> str:
    with open(filename) as f:
        json_file = json.load(f)
    sprecher_name = [json_file[index]["name"] for index in range(len(json_file))]
    return sprecher_name

def extract_sprecherdaten_zusatz(filename):
    with open(filename) as f:
        json_file = json.load(f)
    sprecher_zusatz = [json_file[index]["zusatz"] for index in range(len(json_file))]
    return sprecher_zusatz

def if_string_extract_sprechbeitrag(sprecher_name, sprecher_zusatz) -> bool:
    with open("data/wahlperiode_1_inhalt/wahlperiode_1_inhalt_2.txt") as doc:
        datafile = doc.readlines()
    for line in datafile:
        for name in sprecher_name:
                for zusatz in sprecher_zusatz:
                    if str(zusatz + name) in line:
                        print(line)
                        return True
    return False


def extract_top_from_vector(feature_names, sorted_items, num: int=10) -> dict:
    # get the feature names and tf-idf score of top n items
    return dict([
        [round(score, 3), feature_names[idx]
    ] for score, idx in sorted_items[:num]])

# BENUTZT?
def extract_zwischenfragen(path, file, string_ges) -> None:
    with open(path + file, "r") as f:
        current_line = 1
    zwischenfragen_count = 1
    content = f.readlines()
    for line in [line for line in content if string_ges in line]:
        if string_ges in line:
            with open(str(content[current_line - 2: current_line + 20]), "w+") as f:
                f.write(f"data/extracted_zwischenfragen/zwischenfrage_{zwischenfragen_count}_{file}")
            zwischenfragen_count += 1
        current_line += 1

def remove_Ausschlussbegriffe(keywords_dict, ausschlussbegriffe_liste) -> None:
    for item in keywords_dict:
        for ausschlussbegriff in ausschlussbegriffe_liste:
            if ausschlussbegriff in item:
                del keywords_dict[item]


