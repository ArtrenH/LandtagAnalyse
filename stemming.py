import os
from tqdm import tqdm

from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer


def tokenizing(path: str, filename: str) -> list[str]:
    with open(f"{path}{filename}", 'r', encoding='utf-8', errors='ignore') as files:
        content = files.read()
    words = word_tokenize(content)
    return words

def stemming(words: list[str]) -> list[str]:
    stemmer = SnowballStemmer("german")
    stemmed_words = [] 
    for word in words:
        sw = stemmer.stem(word)
        stemmed_words.append(sw)
    return stemmed_words             

def stem_all(resumable: bool=True) -> None:
    os.makedirs(f"data/cleaned_content_stemmed", exist_ok=True)
    for file in tqdm([elem for elem in os.listdir("data/cleaned_content/") if elem.startswith("i")]):
        if resumable and os.path.exists(f"data/cleaned_content_stemmed/{file}"):
            continue
        content = tokenizing("data/cleaned_content/", file)
        content = stemming(content)
        content = ' '.join(content)
        with open(f"data/cleaned_content_stemmed/{file}", "w+") as f:
            f.write(content)
      
if __name__ == "__main__":
    stem_all()

