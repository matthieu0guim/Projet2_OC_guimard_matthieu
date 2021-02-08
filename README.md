# Titre de projet

## Description
This programme has been redacted for web scraping purpose. It is focused
for the website book.toscrape.com. It will load the html code of a given category.
Then, the programme will open and parse the webpage corresponding to each book in 
the category. Once done it will load the following informations:
-product_page_url

-universal_product_code

-title

-price_including_taxes

-price_excluding_taxes

-number_available

-product_description

-category

-review_rating

-image_url
All these informations will be loaded in a .csv file.
The script will ask how many categories the user want to investigate.
Then it will ask to name them. Once done, the script will load the previous informations in the same .csv file.


## Execution
### démarrer environnement virtuel 
The first step is to create a virtual environment in order to install the required libraries.

1- create your environment with the command "py -m venv env"

2- activate it with the command "env\script\activate"

3- install the needed libraries with the command "pip install -r requirements.txt"

### éxécuter le script
```sh
py plsr_pages.py 
```

## Dependances


## Licences
the MIT license (MIT)