import requests
from bs4 import BeautifulSoup

"""
ce code a pour but d'améliorer le code ninja.py pour enregistrer les infos dans un fichier csv.
"""
product_description = ""
product_page_url = "http://books.toscrape.com/catalogue/olio_984/index.html"  # on donne l'url à une variable
r = requests.get(product_page_url) # méthode de requests qui tire de l'information depuis l'url
page = BeautifulSoup(r.text, 'html.parser') # on extrait le texte qu'il y a dans la variable r
title = page.find('div', {'class' : 'col-sm-6 product_main'}).find('h1')
core = list(page.find_all('p'))
noms = page.findAll('th')
category = page.find('a', {'href' : '../category/books/poetry_23/index.html'})
item = page.find('div', {'class': 'col-sm-6 product_main'}).findAll({'p'})
review_rating = item[2].get('class')[1]
photo = page.find('div', {'class': 'item active'})
image_url = photo.img.get("src")
infos = page.find('table', {'class' : 'table table-striped'})

"""
   Dans cette boucle for j'ai préalablement affiché la valeur de i pour chaque valeur de n.
   Lorsque cette valeur correspondait à l'info que je cherchais j'ai attribué la valeur à la variable correspondante.
   Cette méthode est empirique et est donc par définition vulnérable devant un cas particulier comme par exemple un 
   ordre des infos différents
"""
for n,i in enumerate(infos):

    if n == 1:
        upc = i.find('td')

    elif n == 5:
        price_excluding_taxes = i.find('td')

    elif n == 7:
        price_including_taxes = i.find('td')

    elif n == 11:
        number_available = i.find('td').text.replace('(','').split()[2]

for c in core:
    if len(c.text) > 200:
        product_description = c.text
        break


with open('page_produit.csv', 'w', encoding='utf8') as outf:
    outf.write('product_page_url, universal_product_code, title, price_including_taxes, price_excluding_taxes, '
               'number_available, product_description, category, review_rating, image_url\n')
    outf.write(product_page_url + ',' + upc.text + ',' + title.text + ',' + price_including_taxes.text[1:] + ',' +
               price_excluding_taxes.text[1:] + ',' + number_available + ',' + product_description + ',' + category.text
                + ',' + review_rating + ',' + image_url)


#
# print('titre:', '\n', title.text.split()[0])
# print("product_description:", '\n', str(product_description))
# print("review_rating :", '\n', review)
# [print(str(nom.text), ':', '\n', str(info.text) + '\n\n') for nom, info in zip(noms, infos)]
# print("image_url :", '\n', image_url)
