# Stock scraper - sentient analysis


import requests
from bs4 import BeautifulSoup

URL = 'https://boards.4channel.org/biz/catalog'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

print(soup)




























# EOF
