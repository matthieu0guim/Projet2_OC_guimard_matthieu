import requests
from bs4 import BeautifulSoup
import urllib.request
import os


maintenance = {
    'columns': 'product_page_url; universale_product_code; title; price_including_taxes; '
               'price_excluding_taxes; '
               'number_available; product_description; category; review_rating; image_url; image',
    'csv separator': ';'
}


def find_book_data(url, k):
    dictionary = {'product_page_url': url}

    # with the methode .get, one get an response object with a lot of informations as the status code of the url and else.
    response = requests.get(url)

    # one of these data is the html text that generate the web page. We access this text with the library BeautifulSoup.
    # The methode .content.decode('utf-8', 'ignore') allow us to upload a text with characters only supported in the
    # utf8 encoding methode.
    book_html_info = BeautifulSoup(response.content.decode('utf-8','ignore'), 'html.parser')
    dictionary["title"] = book_html_info.find('div', {'class': 'col-sm-6 product_main'}).find('h1').text
    core = book_html_info.find('article', {'class': 'product_page'}).find_next('p').find_next('p').find_next('p').find_next('p')
    dictionary["category"] = book_html_info.find('ul', {'class': 'breadcrumb'}).find_next('li').find_next('li').find_next(
        'li').find('a').text
    item = book_html_info.find('div', {'class': 'col-sm-6 product_main'}).findAll({'p'})
    dictionary["review_rating"] = item[2].get('class')[1]

    # The following command only take the text from the fifth element because the image url is not completely provided
    # in the html. It comes with ../../ at the beginning. One must delete these characters.
    dictionary["image_url"] = f"http://books.toscrape.com/{book_html_info.find('div', {'class': 'item active'}).img.get('src')[5:]}"
    dictionary['image'] = f"{k}.jpg"
    dictionary["product_description"] = core.text.replace(';', ',')

    # the variable info_table contains the universal_product_code, the price including and excluding taxes and the
    # number of book available.
    info_table = book_html_info.find('table', {'class': 'table table-striped'})
    for index, tr in enumerate(info_table):
        if index == 1:
            dictionary["universale_product_code"] = tr.find('td').text
        elif index == 5:
            dictionary["price_excluding_taxes"] = tr.find('td').text[2:]
        elif index == 7:
            dictionary["price_including_taxes"] = tr.find('td').text[2:]
        elif index == 11:
            dictionary["number_available"] = tr.find('td').text.replace('(', '').split()[2]
    return dictionary


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
        dic['book' + str(n)] = i
    return dic


if __name__ == "__main__":


    home_url = "http://books.toscrape.com/index.html"
    response = requests.get(home_url)
    html_info = BeautifulSoup(response.text, 'html.parser')
    categories = html_info.find('ul', {'class': 'nav nav-list'}).find('ul').find_all('a')
    liste = [i.text.replace('\n', '').strip() for i in categories]

    files_list = []
    for nb, category in enumerate(liste):
        category_folder = f"data/{category}"
        if not os.path.exists(category_folder):
            os.mkdir(category_folder)

        with open(f"data/{category}/page_produit_{category}.csv", 'w', encoding='utf8') as outf:
            files_list.append(f"data/{category}/page_produit_{category}.csv")
            keys = maintenance['columns'].split(';')
            for n, header in enumerate(keys):
                if n == len(keys) - 1:
                    outf.write(header + '\n')
                else:
                    outf.write(header + maintenance['csv separator'])
        with open('.gitignore', 'a', encoding = 'utf8') as ignore:
            ignore.write(f"page_produit_{category}.csv" + '\n')
        home_cat_url = f"http://books.toscrape.com/catalogue/category/books/" \
                       f"{category.lower().replace(' ', '-')}_{nb + 2}/index.html"
        response = requests.get(home_cat_url)
        html_info_cat = BeautifulSoup(response.text, 'html.parser')
        liens = []
        urls = []
        if html_info_cat.find('li', {'class': 'current'}):
            number_of_pages = [f"{home_cat_url.replace('index.html', '')}page-{i}.html"
                               for i in range(1, int(html_info_cat.find('li',
                                                                        {'class': 'current'}).text.strip()[-1]) + 1)]
            link_dictionary = {}
            for url in number_of_pages:
                link_dictionary = listing(url, urls)
            print("if ok")
            for k, v in link_dictionary.items():
                product_inspection = find_book_data(v, k)
                urllib.request.urlretrieve(product_inspection['image_url'],
                                           f"{category_folder}/"
                                           f"{k}.jpg")
                write_data(product_inspection, files_list[nb])
        else:
            number_of_pages = [home_cat_url]
            for url in number_of_pages:
                link_dictionary = listing(url, urls)
            print("else ok")
            for k, v in link_dictionary.items():
                product_inspection = find_book_data(v, k)
                urllib.request.urlretrieve(product_inspection['image_url'],
                                           f"{category_folder}/"
                                           f"{k}.jpg")
                write_data(product_inspection, files_list[nb])

