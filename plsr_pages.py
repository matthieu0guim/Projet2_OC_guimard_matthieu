import requests
from bs4 import BeautifulSoup

"""cette fonction renvoie simplement l'élément dune liste correspondant à l'indice demandé. La seul particularité est"""

maintenance = {'columns': 'product_page_url; universale_product_code; title; price_including_taxes; '
                          'price_excluding_taxes; '
                          'number_available; product_description; category; review_rating; image_url\n'
    , 'csv separator': ';'}
"""This function simply return the element of liste corresponding to the asked indice"""


def lien(liste, i):
    if i > 0:
        return liste[i - 1]


"""the function find_data(v) will parse the html code of a product page and save the text corresponding
to the inquired information into a variable with an explicit name. The 'v' variable is the 
url of the product page used to open the webpage"""


def find_data(v):
    dictionary = {}

    dictionary['product_page_url'] = v  # on donne l'url à une variable
    request = requests.get(dictionary['product_page_url'])  # méthode de requests qui tire de l'information depuis l'url
    page = BeautifulSoup(request.text, 'html.parser')  # on extrait le texte qu'il y a dans la variable r
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
            dictionary["universale_product_code"] = i.find('td').text

        elif n == 5:
            dictionary["price_excluding_taxes"] = i.find('td').text[2:]

        elif n == 7:
            dictionary["price_including_taxes"] = i.find('td').text[2:]

        elif n == 11:
            dictionary["number_available"] = i.find('td').text.replace('(', '').split()[2]
    return dictionary  #


""" The function write_data(dd) will open a .csv file and write the data collected by find_data()
The variable dd is the dictionary created with the find_data() function. As a dictionary is not
sorted, one have to be vigilant when we call a key. This is why the function create a list with 
the header of each column sorted."""


def write_data(dd):

    with open("page_produit.csv", 'a', encoding='utf8') as outdata:
        keys = maintenance['columns'].replace('\n', '').replace(' ', '').split(';')
        for v in keys:
            outdata.write(dd[v] + ';')
        outdata.write("\n")


def initialisation():
    with open('page_produit.csv', 'w', encoding='utf8')as outf:
        keys = maintenance['columns'].replace('\n', '').replace(' ', '').split(';')
        for header in keys:
            outf.write(header)
        outf.write('\n')


welcome_url = f"http://books.toscrape.com/catalogue/category/books/poetry_23/index.html"
response = requests.get(welcome_url)
html_info = BeautifulSoup(response.text, 'html.parser')
book_number = html_info.find('form', {'class': 'form-horizontal'}).find(
    'strong').text  # we identify the number of book in the category.
balises = html_info.find('section').findAll('h3')
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

initialisation()
for k, v in dico_livres.items():
    product_inspection = find_data(v)

    write_data(product_inspection)
