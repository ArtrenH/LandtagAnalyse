import os
import json
from utils import extract_wahlperiode, extract_sitzungsnummer, extract_zwischenfragen

# SITZUNGSLÄNGEN
def count_lines(filename) -> int:
    with open(filename) as f:
        return len(f.read().split("\n"))

def count_words(filename) -> int:
    with open(filename) as f:
        return len(f.read().split())


path = "data/content_wahlperioden"
dirs = [elem for elem in os.listdir("data/content_wahlperioden") if elem.startswith("i")]

def extract_sitzungslaengen(wahlperiode: int=1) -> None:
    wahlperiode_dict = {}
    for file in dirs:
        if int(extract_wahlperiode(file)) == wahlperiode:
            wahlperiode_dict[extract_sitzungsnummer(file)] = count_words(f"{path}/{file}")
    with open(f'data/Sitzungslänge/Sitzungslängen_Wahlperiode_{wahlperiode}.csv', 'w') as f:
        json.dump(wahlperiode_dict, f, indent=4)

def extract_all_wahlperioden() -> None:
    for i in range(1, 7+1):
        extract_sitzungslaengen(i)

if __name__ == "__main__":
    extract_all_wahlperioden()

# UNTERBRECHUNGEN
dirs = [elem for elem in os.listdir("data/content_wahlperioden") if elem.startswith("i")]

def extract_unterbrechungen(partei: str="CDU", wahlperiode: int=7, ignore_beifall: bool=True) -> None:
    partei_dict = {}
    for file in dirs:
        if int(extract_wahlperiode(file)) == wahlperiode:
            with open(f"{path}/{file}", "r") as f:
                content = f.read()   
            interruptions = [par for par in content.split("\n\n") if (len(par.strip()) > 0) and (par.strip()[0]=="(")]
            parteiunterbrechungen = [element for element in interruptions if partei in element]
            if ignore_beifall:
                parteiunterbrechungen = [element for element in parteiunterbrechungen if "Beifall" not in element]
                parteiunterbrechungen = [element for element in parteiunterbrechungen if "Saal" not in element]
            partei_dict[extract_sitzungsnummer(file)] = len(parteiunterbrechungen)
    os.makedirs(f"data/Unterbrechungen{ignore_beifall*'_ohne_Beifall'}/Wahlperiode_{wahlperiode}", exist_ok=True)
    with open(f"data/Unterbrechungen{ignore_beifall*'_ohne_Beifall'}/Wahlperiode_{wahlperiode}/{partei}.json", 'w+') as f:
        json.dump(partei_dict, f, indent=4)

def extract_all_unterbrechungen() -> None:
    for partei in ["CDU", "SPD", "PDS", "NPD", "FDP", "AfD", "LINKEN", "F.D.P.", "Linksfraktion", "Bündnis 90", "GRÜNEN"]:
        for wahlperiode in range(1,7+1):
            extract_unterbrechungen(partei, wahlperiode)

if __name__ == "__main__":
    extract_all_unterbrechungen()


    # ZWISCHENFRAGEN:

    dirs = os.listdir("data/content")

    for file in dirs[:2]:
        extract_zwischenfragen("data/content/", file, "Zwischenfrage")