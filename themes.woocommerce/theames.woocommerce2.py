from csv import writer
import csv
from distutils.command.build_scripts import first_line_re
from encodings import utf_8
from tkinter import FIRST
from numpy import product
import requests
from bs4 import BeautifulSoup


def get_product_link(page):
    url = f'https://themes.woocommerce.com/storefront/product-category/clothing/page/{page}'
    links=[]
    r = requests.get(url)
    page = BeautifulSoup(r.text,'html.parser')
    products = page.find('ul',{'class':'products'})
    lists = products.find_all('li')
    #print(lists)
    for item in lists:
        link=item.find('a')['href']
        links.append(link)

    return links

def parse_product(url):
    
    r = requests.get(url)
    page = BeautifulSoup(r.text,'html.parser')
    title = page.find('h1',class_='product_title entry-title').text
    price = page.find('p',class_='price').text
    try:
        sku = page.find('span',class_='sku').text
    except AttributeError as err:
        sku='none'
    category = page.find('span',class_='posted_in').text[10:]

    product ={
        'title':title,
        'price':price,
        'sku':sku,
        'category':category
    }

    return product

def save_csv(result):
    keys=result[0].keys()

    with open('product.csv','w',encoding= 'utf8' , newline='') as f:
        dict_writer= csv.DictWriter(f,keys)
        dict_writer.writeheader()
        dict_writer.writerows(result)


def main():
    result=[]
    for x in range(1,6):
        print('Getting Page: ',x)
        urls=get_product_link(x)
        for url in urls:
            result.append(parse_product(url))
        print('Total Result: ',len(result))
        save_csv(result)

if __name__ == '__main__':
    main()