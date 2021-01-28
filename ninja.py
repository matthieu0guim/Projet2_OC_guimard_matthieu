import requests
from bs4 import BeautifulSoup
url = "http://books.toscrape.com/catalogue/olio_984/index.html"
r = requests.get(url)
title = BeautifulSoup(r.text, 'html.parser').find('title')
print(title.text)
infos = BeautifulSoup(r.text, 'html.parser').findAll('td')
[print(str(info.text) + '\n\n') for info in infos]
