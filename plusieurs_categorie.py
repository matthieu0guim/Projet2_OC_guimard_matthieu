import requests
from bs4 import BeautifulSoup

maintenance = {'columns': 'product_page_url; universale_product_code; title; price_including_taxes; '
                          'price_excluding_taxes; '
                          'number_available; product_description; category; review_rating; image_url\n'
    , 'csv separator': ';'}

home_url = "http://books.toscrape.com/index.html"
response = requests.get(home_url)
html_info = BeautifulSoup(response.text, 'html.parser')


categories = html_info.find('ul', {'class': 'nav nav-list'}).find('ul').find_all('a')
liste = []
for i in categories:
    liste.append(i.text.replace('\n', '').strip())
print(liste)

for n, i in enumerate(liste):
    with open(f"page_produit_{i}.csv", 'w', encoding='utf8') as outf:
        keys = maintenance['columns'].replace('\n', '').replace(' ', '').split(';')
        for n, header in enumerate(keys):
            if n == len(keys) - 1:
                outf.write(header)
            else:
                outf.write(header + maintenance['csv separator'])
        outf.write('\n')