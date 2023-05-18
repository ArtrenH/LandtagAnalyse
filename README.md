# LandtagAnalyse

# Ziel des Projekts

In diesem Repository werden Plenatprotokolle des sächsischen Landtags von 1990 bis zur 7. Wahlperiode ausgewertet.

# Execution

- Clone the Repo and cd into it:
```sh
git clone https://github.com/ArtrenH/LandtagAnalyse.git 
cd LandtagAnalyse
```
- create a python virtual environment: (you need to have installed python for this)
```sh
python3 -m venv venv
source venv/bin/activate
```
- install the required libraries:
```sh
pip3 install -r requirements.txt
```
- exexute the preperation files:
```sh
python3 preparation.py
```
- now execute the remaining files to replicate the data:
```sh
python3 stemming.py
python3 keyword_extraction.py
python3 keywords_dokumente_auswertung.py
```
