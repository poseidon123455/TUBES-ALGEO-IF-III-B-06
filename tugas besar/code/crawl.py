import argparse
import string
import sys
from datetime import datetime, timedelta
from pathlib import Path

import requests
from bs4 import BeautifulSoup


# scrapping
def scraping(data):
    path = Path()/"../data/crawl"/f'data{data[0]}.txt'
    with open(path, 'w') as file:
        soup = BeautifulSoup(requests.get(data[1]).text, 'html.parser')
        isi = soup.select_one('#contentx')
        for i in isi('script'):
            i.decompose()
        title = soup.select_one('.title').get_text().strip()
        isi = isi.get_text().strip()  
        data[2].write(data[1]+'\n')
        file.write(title+'\n')
        file.write(isi)

# argument
arg = argparse.ArgumentParser()
option = arg.add_mutually_exclusive_group()
option.add_argument("-p", "--page-limit",help="limit file by number of files", type=int)
args = vars(arg.parse_args())

# Url
urlberita = "https://www.cnnindonesia.com/nasional/20230105201518-20-896783/tetangga-ungkap-pemilik-rumah-mewah-cakung-jual-pot-bunga-untuk-beras"

# tanggal hari ini
date = datetime.today()

# batasi jumlah page yang akan di crawling
page, page_limit = 0, args['page_limit'] if args['page_limit'] != None else None

# buka folder link untuk menyimpan link dari url yg di crawl dan lakukan looping
with open('../data/link/link.txt',"w") as buka:
    while True:
        link = f'{urlberita}{date.strftime("%Y/%m/%d")}'
        while True:
            print(f'Getting url from : {link}')
            soup = BeautifulSoup(requests.get(link).text.encode('utf-8'), 'html.parser')
            print("Url found      : ", len(soup.select('.f17')))
            for url in soup.select('.f17'):
                urls = url.find('a')['href']
                try:
                    # scrapping url
                    scraping([page, url, buka])
                except AttributeError:
                    print('error atribute..')
                page += 1
                if page == page_limit:
                    sys.exit(f'Program reach maximum {page_limit} page')
            else:
                break
        # lanjut ke tanggal berikutnya
        date += timedelta(days=-1)
