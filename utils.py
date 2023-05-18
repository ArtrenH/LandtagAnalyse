import json

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

# WHAT DOES THIS DO?
def extract_sprecherdaten_zusatz(filename: str) -> list:
    with open(filename) as f:
        json_file = json.load(f)
    sprecher_zusatz = [json_file[index]["zusatz"] for index in range(len(json_file))]
    return sprecher_zusatz

def if_string_extract_sprechbeitrag(sprecher_name: list[str], sprecher_zusatz: list[str]) -> bool:
    with open("data/wahlperiode_1_inhalt/wahlperiode_1_inhalt_2.txt") as doc:
        datafile = doc.readlines()
    for line in datafile:
        for name in sprecher_name:
            for zusatz in sprecher_zusatz:
                if str(zusatz + name) in line:
                    print(line)
                    return True
    return False

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

