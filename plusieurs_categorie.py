import requests
from bs4 import BeautifulSoup

maintenance = {
    'columns': 'product_page_url; universale_product_code; title; price_including_taxes; '
               'price_excluding_taxes; '
               'number_available; product_description; category; review_rating; image_url',
    'csv separator': ';'
}


def find_book_data(url):
    dictionary = {'product_page_url': url}

    # méthode de requests qui tire de l'information depuis l'url
    response = requests.get(url)
    if response.ok:
        print(url, "[ok]")
    else:
        print(url, "[ko]")

    # on extrait le texte qu'il y a dans la variable response
    page = BeautifulSoup(response.text, 'html.parser')
    dictionary["title"] = page.find('div', {'class': 'col-sm-6 product_main'}).find('h1').text

    core = page.find('article', {'class': 'product_page'}).find_next('p').find_next('p').find_next('p').find_next('p')

    dictionary["category"] = page.find('ul', {'class': 'breadcrumb'}).find_next('li').find_next('li').find_next(
        'li').find('a').text
    # print(dictionary["category"])
    item = page.find('div', {'class': 'col-sm-6 product_main'}).findAll({'p'})
    dictionary["review_rating"] = item[2].get('class')[1]
    photo = page.find('div', {'class': 'item active'})
    dictionary["image_url"] = photo.img.get("src")
    infos = page.find('table', {'class': 'table table-striped'})
    dictionary["product_description"] = core.text.replace(';', ',')
    for index, tr in enumerate(infos):

        if index == 1:
            dictionary["universale_product_code"] = tr.find('td').text

        elif index == 5:
            dictionary["price_excluding_taxes"] = tr.find('td').text[2:]

        elif index == 7:
            dictionary["price_including_taxes"] = tr.find('td').text[2:]

        elif index == 11:
            dictionary["number_available"] = tr.find('td').text.replace('(', '').split()[2]
    return dictionary  #


def write_data(data, name):
    with open(f"{name}", 'a', encoding='utf8') as outdata:
        keys = maintenance['columns'].replace('\n', '').replace(' ', '').split(';')
        for k in keys:
            outdata.write(data[k] + ';')
        outdata.write("\n")


def listing(u, inventory):
    welcome_url = f"{u}"
    response = requests.get(welcome_url)
    html = BeautifulSoup(response.text, 'html.parser')

    balises = html.find('section').findAll('h3')

    links = []
    for i in balises:
        links.append(i.find('a').get('href').split('/')[-2:])

    TITRE_LIVRE = 0
    INDEX_PAGE = 1

    for i in links:
        inventory.append(f"http://books.toscrape.com/catalogue/{i[TITRE_LIVRE]}/{i[INDEX_PAGE]}")

    dic = {}
    for n, i in enumerate(inventory):
        dic['livre' + str(n)] = i
    return dic


if __name__ == "__main__":
    home_url = "http://books.toscrape.com/index.html"
    response = requests.get(home_url)
    html_info = BeautifulSoup(response.text, 'html.parser')

    categories = html_info.find('ul', {'class': 'nav nav-list'}).find('ul').find_all('a')

    liste = []
    for i in categories:
        liste.append(i.text.replace('\n', '').strip())

    files_list = []
    for n, i in enumerate(liste):
        with open(f"page_produit_{i}.csv", 'w', encoding='utf8') as outf:
            files_list.append(f"page_produit_{i}.csv")
            keys = maintenance['columns'].split(';')
            for n, header in enumerate(keys):
                if n == len(keys) - 1:
                    outf.write(header + '\n')
                else:
                    outf.write(header + maintenance['csv separator'])

    for nb, cat in enumerate(liste):
        home_cat_url = f"http://books.toscrape.com/catalogue/category/books/{cat.lower().replace(' ', '-')}_{nb + 2}/index.html"
        response = requests.get(home_cat_url)
        html_info_cat = BeautifulSoup(response.text, 'html.parser')

        dico_livres = {}
        liens = []
        urls = []
        if html_info_cat.find('li', {'class': 'current'}):
            # print("home_cat_url:", home_cat_url)
            number_of_pages = [f"{home_cat_url.replace('index.html', '')}page-{i}.html"
                               for i in range(1, int(html_info_cat.find('li', {'class': 'current'}).text.strip()[-1]) + 1)]
            # print("nombre de page:", number_of_pages)
            link_dictionary = {}
            for url in number_of_pages:
                link_dictionary = listing(url, urls)

            print("if ok")

            for k, v in link_dictionary.items():
                product_inspection = find_book_data(v)


                write_data(product_inspection, files_list[nb])

        else:
            number_of_pages = [home_cat_url]
            for url in number_of_pages:

                link_dictionary = listing(url, urls)
            print("else ok")
            for k, v in link_dictionary.items():
                product_inspection = find_book_data(v)

                write_data(product_inspection, files_list[nb])

