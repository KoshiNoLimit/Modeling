import time
import geckodriver_autoinstaller
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np
from selenium import webdriver


geo_path = 'https://geogoroda.ru'
region = '/region/moskovskaya-oblast'
index_path = 'https://индекс-городов.рф/#/regions/116'


def get_geo_stats():
    response = requests.get(geo_path + region)
    soup = BeautifulSoup(response.text, 'lxml')

    body = soup.find('tbody')
    rows = body.find_all('tr', attrs={'class': re.compile('even|odd')})

    cities = []

    for i in np.arange(len(rows)):
        link = rows[i]\
            .find_next('td') \
            .find_next_sibling() \
            .find('a')
        href = link['href']
        name = link.text
        print(name)

        city_response = requests.get(geo_path + href)
        city_soup = BeautifulSoup(city_response.text, 'lxml')

        city_body = city_soup.find('div', attrs={
            'class': 'views-row views-row-1 views-row-odd views-row-first views-row-last views-field-tooltip-row'})

        area = city_body\
            .find('div', attrs={'class': 'views-field views-field-field-ploshad-goroda'}) \
            .find('div', attrs={'class': 'field-content'}).text
        area = re.search('(\d+ )*[\d\.]+', area).group(0)

        density = city_body\
            .find('div', attrs={'class': 'views-field views-field-field-plotnost'}) \
            .find('div', attrs={'class': 'field-content'}).text
        density = re.search('(\d+ )*[\d\.]+', density).group(0).replace(' ', '')

        cities.append([name.replace('ё', 'е'), area, density])
    return pd.DataFrame(
        np.array(cities),
        columns=['name', 'area', 'density'])


def load_indexes():
    geckodriver_autoinstaller.install()

    browser = webdriver.Firefox()
    browser.get(index_path)
    time.sleep(2)
    generated_html = browser.page_source
    browser.quit()

    soup = BeautifulSoup(generated_html, 'lxml')
    table = soup.find('div', attrs={'class': 'sc-hmXxxW eZveiC sc-fzsDOv bzadXW'})
    cities = table.find_all('a', attrs={'class': 'sc-jVODtj iavBPH'})

    return pd.DataFrame(
        np.array([[a.text[:-3].replace('ё', 'е'), a.text[-3:]] for a in cities]),
        columns=['name', 'index'])


stats = get_geo_stats()
indexes = load_indexes()

data = pd.merge(stats, indexes, on='name', how='inner')
data.to_csv('towns/towns.csv', index=False)
