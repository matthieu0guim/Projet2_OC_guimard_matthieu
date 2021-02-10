import requests
from bs4 import BeautifulSoup

maintenance = {'columns': 'product_page_url; universale_product_code; title; price_including_taxes; '
                          'price_excluding_taxes; '
                          'number_available; product_description; category; review_rating; image_url\n'
    , 'csv separator': ';'}

home_url = "http://books.toscrape.com/catalogue/category/books/mystery_3/page-1.html"
response = requests.get(home_url)
html_info = BeautifulSoup(response.text, 'html.parser')

def lien(liste, i):
    if i > 0:
        return liste[i - 1]


def find_data(v):
    dictionary = {}

    dictionary['product_page_url'] = v  # on donne l'url à une variable
    request = requests.get(dictionary['product_page_url'])  # méthode de requests qui tire de l'information depuis l'url
    page = BeautifulSoup(request.text, 'html.parser')  # on extrait le texte qu'il y a dans la variable r
    dictionary["title"] = page.find('div', {'class': 'col-sm-6 product_main'}).find('h1').text

    core = page.find('article', {'class': 'product_page'}).find_next('p').find_next('p').find_next('p').find_next('p')
    noms = page.findAll('th')
    dictionary["category"] = page.find('ul', {'class': 'breadcrumb'}).find_next('li').find_next('li').find_next('li').find('a').text
    #print(dictionary["category"])
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
def write_data(dd):

    with open("page_produit.csv", 'a', encoding='utf8') as outdata:
        keys = maintenance['columns'].replace('\n', '').replace(' ', '').split(';')
        for v in keys:
            outdata.write(dd[v] + ';')
        outdata.write("\n")
def initialisation():
    with open('page_produit.csv', 'w', encoding='utf8')as outf:
        keys = maintenance['columns'].replace('\n', '').replace(' ', '').split(';')
        for n, header in enumerate(keys):
            if n == len(keys)-1:
                outf.write(header)
            else:
                outf.write(header + maintenance['csv separator'])
        outf.write('\n')
def listing(u, inventory):

    welcome_url = f"{u}"
    response = requests.get(welcome_url)
    html = BeautifulSoup(response.text, 'html.parser')


    balises = html.find('section').findAll('h3')
    print(balises)
    links = []
    for i in balises:
        links.append(i.find('a').get('href').split('/')[-2:])
    print(len(links))

    TITRE_LIVRE = 0
    INDEX_PAGE = 1


    for i in links:
        inventory.append(f"http://books.toscrape.com/catalogue/{i[TITRE_LIVRE]}/{i[INDEX_PAGE]}")
    print(len(inventory), inventory)
    dic = {}
    for n,i in enumerate(inventory):
        dic['livre' + str(n)] = i
    return dic





initialisation()
dico_livres = {}
liens = []
urls = []
n = 0

if html_info.find('li', {'class': 'current'}):
    number_of_pages = [f"http://books.toscrape.com/catalogue/category/books/mystery_3/page-{i}.html"
                       for i in range(1,int(html_info.find('li', {'class': 'current'}).text.strip()[-1])+1)]
    for i, url in enumerate(number_of_pages):
        link_dictionary = listing(url, urls)

    initialisation()
    for k, v in link_dictionary.items():
        product_inspection = find_data(v)

        write_data(product_inspection)


else:
    number_of_pages = [home_url]
    for i, url in enumerate(number_of_pages):
        link_dictionary = listing(url, dico_livres, urls, n)
    for k, v in link_dictionary.items():
        product_inspection = find_data(v)

        write_data(product_inspection)





# for n, i in enumerate(categories):
#     with open(f"page_produit_{i}.csv", 'w', encoding='utf8') as outf:
#         keys = maintenance['columns'].replace('\n', '').replace(' ', '').split(';')
#         for n, header in enumerate(keys):
#             if n == len(keys) - 1:
#                 outf.write(header)
#             else:
#                 outf.write(header + maintenance['csv separator'])
#         outf.write('\n')