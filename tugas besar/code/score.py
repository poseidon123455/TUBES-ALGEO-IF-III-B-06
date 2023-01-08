from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from pathlib import Path
from tqdm import tqdm
import os
import sys
import math


def index(hashs, lists):
    for i in lists:
        if i in hashs:
            hashs[i] += 1
        else:
            hashs[i] = 1


# stopword dalam bahasa indonesian
get_stopword = StopWordRemoverFactory()
stopwords = get_stopword.create_stop_word_remover()

# stemming dalam bahasa indonesian
get_stemmer = StemmerFactory()
stemmer = get_stemmer.create_stemmer()

# hash
tf, df, idf, kalimatUtama, judul = dict(), dict(), dict(), dict(), dict()

if os.path.exists('../data/clean'):
    print(f'Directory : ../data/clean')
    for f in tqdm(Path('../data/clean').glob("*.txt")):
        name = str(f).split('/')
        df[name[3]], kalimatUtama[name[3]], judul[name[3]] = dict(), dict(), dict()

        File = open(f, 'r').read()
        File = stopwords.remove(File)

        sentence = File.split('\n')
        title = stemmer.stem(sentence[0].lower()).split()
        main = stemmer.stem(sentence[1].lower()).split()
        hasil = stemmer.stem(File.lower()).split()

        index(judul[name[3]], title)
        index(kalimatUtama[name[3]], main)
        index(tf, hasil)
        index(df[name[3]], hasil)
else:
    print("Wrong directory path")
    sys.exit(1)

print(f'unique words : {len(tf)}\n')

with open('../data/index/index.txt', 'w') as file:
    for term, freq in tqdm(tf.items()):
        idf[term] = 1 + math.log10(len(df)/tf[term])
        file.write(f"{term}")
        for doc, tfdoc in df.items():
            if term in tfdoc:
                if term in judul[doc]:
                    weigth = (tfdoc[term] * idf[term])*1
                elif term in kalimatUtama[doc]:
                    weigth = (tfdoc[term] * idf[term])*2/3
                else:
                    weigth = (tfdoc[term] * idf[term])*1/3
            else:
                file.write(f' {doc}:0')
                continue
            file.write(f' {doc}:{weigth}')
        file.write('\n')
print('done')