from pathlib import Path
from string import punctuation
import os
import sys

def hapus(data):
    with open(f'../data/clean/{data[1]}', 'w') as buka:
        for index, line in enumerate(data[0].split('\n')):
            if index is 1:
                main_sentence = line.split('.')
                try:
                    buka.write(main_sentence[0].translate(str.maketrans('', '', punctuation))+'\n')
                except IndexError:
                    pass

                for sentence in main_sentence[1:]:
                    buka.write(sentence.translate(str.maketrans('', '', punctuation)))
                continue
            buka.write(line.translate(str.maketrans('', '', punctuation))+'\n')


if os.path.exists('../data/crawl'):
    print(f'Directory : ../data/crawl')
    print('Process...')
    for f in Path('.').glob(f"../data/crawl/*.txt"):
        name = str(f).split('/')
        File = open(f, 'r').read()
        hapus([File, name[3]])
else:
    print("Wrong directory path")
    sys.exit(1)