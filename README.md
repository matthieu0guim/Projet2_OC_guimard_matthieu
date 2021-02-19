# Web-scraping with python.

## Description
This programme has been redacted for web scraping purpose. It is focused
on the website book.toscrape.com. It will load the html code of the home page in order to identify all the categories.
Then, the programme will open the first one and parse it. It will create a list containing the title of all the books of 
the category. It will then open each webpage corresponding to each book.
Once done it will load the following informations:

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
The image file will also be downloaded and saved in the same folder.
To visualize the data, it is possible to open the .csv file with Microsoft Excel.


## Execution
### how to implement the virtual environment:
The first step is to create a virtual environment in order to install the required libraries.

1- create your environment with the command "py -m venv env"

2- activate it with the command "env\script\activate"

3- install the needed libraries with the command "pip install -r requirements.txt"

### script execution:
Get into the correct folder using terminal command. Then run the following command.

```sh
python plusieurs_categorie.py 
```

## Dependencies


## Licences
the MIT license (MIT)