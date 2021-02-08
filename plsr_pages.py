import requests
from bs4 import BeautifulSoup

"""cette fonction renvoie simplement l'élément dune liste correspondant à l'indice demandé. La seul particularité est"""


def lien(liste, i):
    if i > 0:
        return liste[i - 1]

def find_data(v):
    dictionary = {}

    dictionary['product_page_url'] = v  # on donne l'url à une variable
    response = requests.get(dictionary['product_page_url'])  # méthode de requests qui tire de l'information depuis l'url
    page = BeautifulSoup(response.text, 'html.parser')  # on extrait le texte qu'il y a dans la variable r
    dictionary["title"] = page.find('div', {'class': 'col-sm-6 product_main'}).find('h1').text
    core = page.find('article', {'class': 'product_page'}).find_next('p').find_next('p').find_next('p').find_next('p')
    noms = page.findAll('th')
    dictionary["category"] = page.find('a', {'href': '../category/books/poetry_23/index.html'}).text
    item = page.find('div', {'class': 'col-sm-6 product_main'}).findAll({'p'})
    dictionary["review_rating"] = item[2].get('class')[1]
    photo = page.find('div', {'class': 'item active'})
    dictionary["image_url"] = photo.img.get("src")
    infos = page.find('table', {'class': 'table table-striped'})
    dictionary["product_description"] = core.text.replace(';', ',')
    for n, i in enumerate(infos):

        if n == 1:
            dictionary["upc"] = i.find('td').text

        elif n == 5:
            dictionary["price_excluding_taxes"] = i.find('td').text

        elif n == 7:
            dictionary["price_including_taxes"] = i.find('td').text

        elif n == 11:
            dictionary["number_available"] = i.find('td').text.replace('(', '').split()[2]
    return dictionary

welcome_url = f"http://books.toscrape.com/catalogue/category/books/poetry_23/index.html"
r = requests.get(welcome_url)
page = BeautifulSoup(r.text, 'html.parser')
book_number = page.find('form', {'class': 'form-horizontal'}).find(
    'strong').text  # on identifie le nombre de livres dans la categorie
balises = page.find('section').findAll('h3')
liens = []
urls = []
TITRE_LIVRE = 0
INDEX_PAGE = 1
for i in balises:
    liens.append(i.find('a').get('href').split('/')[-2:])

for i in liens:
    urls.append(f"http://books.toscrape.com/catalogue/{i[TITRE_LIVRE]}/{i[INDEX_PAGE]}")





n = 0
dico_livres = {}
while n < len(liens):
    n += 1
    dico_livres['livre ' + str(n)] = lien(urls, n)


i = 0

with open('page_produit.csv', 'w', encoding='utf8') as outf:
    outf.write(f"product_page_url; universal_product_code; title; price_including_taxes; price_excluding_taxes;"
               f"number_available; product_description; category; review_rating; image_url\n")

for k, v in dico_livres.items():

    dictionary = find_data(v)

    with open('page_produit.csv', 'a', encoding='utf8') as outf:
        value = 2
        outf.write(
            dictionary["product_page_url"] + ';' + dictionary["upc"] + ';' + dictionary["title"] + ';' +
            dictionary["price_including_taxes"][value:] + ';' + dictionary["price_excluding_taxes"][value:] + ';' +
            dictionary["number_available"] + ';' + dictionary["product_description"] + ';' + dictionary["category"] +
            ';' + dictionary["review_rating"] + ';' + dictionary["image_url"] + "\n")
