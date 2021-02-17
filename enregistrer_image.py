import requests
from bs4 import BeautifulSoup
import urllib.request
import os

url_page = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

response = requests.get(url_page)
soup = BeautifulSoup(response.text, 'html.parser')

image_url = f"http://books.toscrape.com/{soup.find('div', {'class': 'item active'}).img.get('src')[5:]}"
print(image_url)
os.mkdir('mon_dossier')
urllib.request.urlretrieve(image_url, "mon_dossier/image_test.jpg")