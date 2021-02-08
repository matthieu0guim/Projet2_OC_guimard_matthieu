import requests
from bs4 import BeautifulSoup

welcome_url = "http://books.toscrape.com/catalogue/category/books/poetry_23/index.html"
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
print(urls)

"""cette fonction renvoie simplement l'élément dune liste correspondant à l'indice demandé. La seul particularité est"""


def lien(liste, i):
    if i > 0:
        return liste[i - 1]


n = 0
dico_livres = {}
while n < len(liens):
    n += 1
    dico_livres['livre ' + str(n)] = lien(urls, n)

    # print(dico_livres)
i = 0

with open('page_produit.csv', 'w', encoding='utf8') as outf:
    outf.write('product_page_url, universal_product_code, title, price_including_taxes, price_excluding_taxes, '
               'number_available, product_description, category, review_rating, image_url\n')
for k, v in dico_livres.items():

    product_description = ""
    product_page_url = v  # on donne l'url à une variable
    r = requests.get(product_page_url)  # méthode de requests qui tire de l'information depuis l'url
    page = BeautifulSoup(r.text, 'html.parser')  # on extrait le texte qu'il y a dans la variable r
    title = page.find('div', {'class': 'col-sm-6 product_main'}).find('h1')
    core = list(page.find_all('p'))
    noms = page.findAll('th')
    category = page.find('a', {'href': '../category/books/poetry_23/index.html'})
    item = page.find('div', {'class': 'col-sm-6 product_main'}).findAll({'p'})
    review_rating = item[2].get('class')[1]
    photo = page.find('div', {'class': 'item active'})
    image_url = photo.img.get("src")
    infos = page.find('table', {'class': 'table table-striped'})

    """
           Dans cette boucle for j'ai préalablement affiché la valeur de i pour chaque valeur de n.
           Lorsque cette valeur correspondait à l'info que je cherchais j'ai attribué la valeur à la variable correspondante.
           Cette méthode est empirique et est donc par définition vulnérable devant un cas particulier comme par exemple un 
           ordre des infos différents
        """
    for n, i in enumerate(infos):

        if n == 1:
            upc = i.find('td')

        elif n == 5:
            price_excluding_taxes = i.find('td')

        elif n == 7:
            price_including_taxes = i.find('td')

        elif n == 11:
            number_available = i.find('td').text.replace('(', '').split()[2]

    for c in core:
        if len(c.text) > 200:
            product_description = c.text
            break

    with open('page_produit.csv', 'a', encoding='utf8') as outf:

        outf.write(
            product_page_url + ',' + upc.text + ',' + title.text + ',' + price_including_taxes.text[1:] + ',' +
            price_excluding_taxes.text[
            1:] + ',' + number_available + ',' + product_description + ',' + category.text
            + ',' + review_rating + ',' + image_url + '\n')
