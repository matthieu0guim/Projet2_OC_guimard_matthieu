import requests
from bs4 import BeautifulSoup
"""
ce code a seulement pour but de recueillir de manière grossière les infos qui nous intéressent
sur la page web. La partie csv sera abordée dans un autre programme.
On repère le nom de l'info avec les balises <th> et le contenue de l'info avec les balises <tr>.
On stocke chaque fois dans une liste. On affiche la liste.
"""

url = "http://books.toscrape.com/catalogue/olio_984/index.html" # on donne l'url à une variable
r = requests.get(url) 
title = BeautifulSoup(r.text, 'html.parser').find('title')
print('titre:',title.text[0:10])
noms = BeautifulSoup(r.text, 'html.parser').findAll('th')
infos = BeautifulSoup(r.text, 'html.parser').findAll('td')

[print(str(nom.text), ':', str(info.text) + '\n\n') for nom in noms for info in infos]
