import requests
from bs4 import BeautifulSoup

welcome_url = "http://books.toscrape.com/catalogue/category/books/poetry_23/index.html"
r = requests.get(welcome_url)
page = BeautifulSoup(r.text, 'html.parser')
book_number = page.find('form', {'class' : 'form-horizontal'}).find('strong').text #on identifie le nombre de livres dans la categorie
balises = page.find('section').findAll('h3')
liens = []
urls = []

for i in balises:
    liens.append(i.find('a').get('href').split('/')[-2:])

for i in liens:
    urls.append("http://books.toscrape.com/catalogue/" + i[0] + "/" + i[1])

"""cette fonction renvoie simplement l'élément dune lioste correspondant à l'indice demandé. La seul particularité est"""
def lien(liste,i):
    if i > 0:
        return liste[i-1]

n = 0
dico_livres = {}
while n < len(liens):
    n += 1
    dico_livres['livre ' + str(n)] = lien(urls, n)

    # print(dico_livres)
i = 0


for k,l in dico_livres.items():
    if int(k[-1]) > 2 :
        break
    else:
