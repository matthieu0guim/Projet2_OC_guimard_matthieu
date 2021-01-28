import requests
from bs4 import BeautifulSoup

"""
ce code a seulement pour but de recueillir de manière grossière les infos qui nous intéressent
sur la page web. La partie csv sera abordée dans un autre programme.
On repère le nom de l'info avec les balises <th> et le contenue de l'info avec les balises <tr>.
On stocke chaque fois dans une liste. On affiche la liste.
"""
product_description = ""
product_page_url = "http://books.toscrape.com/catalogue/olio_984/index.html"  # on donne l'url à une variable
r = requests.get(product_page_url)
page = BeautifulSoup(r.text, 'html.parser')
title = page.find('title')
core = list(page.find_all('p'))
noms = page.findAll('th')
infos = page.findAll('td')
cat = page.findAll('a')
categorie = cat[3].text
item = page.find('div', {'class': 'col-sm-6 product_main'}).findAll({'p'})
review = item[2].get('class')[1]
photo = page.find('div', {'class': 'item active'})
image_url = photo.img.get("src")


for c in core:
    if len(c.text) > 200:
        product_description = c.text
        break

print('titre:', '\n', title.text.split()[0])
print("product_description:", '\n', str(product_description))
print("review_rating :", '\n', review)
[print(str(nom.text), ':', '\n', str(info.text) + '\n\n') for nom, info in zip(noms, infos)]
print("image_url :", '\n', image_url)
