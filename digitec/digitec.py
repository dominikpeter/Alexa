import logging
import requests
from lxml import html, etree
from random import randint
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
import re
from bs4 import BeautifulSoup

app = Flask(__name__)
ask = Ask(app, "/digitec")

page = "https://www.digitec.ch/de/Sale"

def get_products(url):
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}
    s = requests.get(page, headers=hdr)

    soup = BeautifulSoup(s.content, 'html.parser')
    overlay = soup.find_all("a", class_="product-overlay")
    x = []
    for j in overlay:
        tag = re.compile("'products': .+", flags=re.DOTALL)
        tag = tag.findall(str(j))
        x.append(tag)
    return x

def product_to_dict(products):
    d = {}
    for i in x:
        j = ''.join(i)
        name = re.compile("'dg_nameWithBrand':.+,")
        price = re.compile("'price':.+,")
        price = '.'.join(re.findall('\d+', ''.join(price.findall(j))))
        names = re.compile('\s.+,')
        names = ''.join(names.findall(''.join(name.findall(j))))
        if names:
            d[names[2:-2]] = float(price)
    return d


@ask.launch
def welcome():
    welcome_msg = render_template('welcome')
    return question(welcome_msg)


@ask.intent("NumberIntent", convert={"Anzahl": int})
def digitec():
    x = get_products(page)
    d = product_to_dict(x)

    output = []
    for i, j in enumerate(d):
        if i <= Anzahl:
            output.append(
               'Das Podukt {} Kostet heute bei Ditgitec {}.'.format(i, d[i]))
    return statement('\n'.join(output))


if __name__ == '__main__':
    app.run(debug=True)
