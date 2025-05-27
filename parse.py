import requests
from bs4 import BeautifulSoup

from db import Database, Flat

url = 'https://re.kufar.by/l/slonim/snyat/kvartiru?cur=USD'


def parse_flats():
    response = requests.get(url)

    if response.status_code != 200:
        raise ValueError('Status code: ', response.status_code)

    soup = BeautifulSoup(response.content, 'html.parser')
    sections = soup.find_all('section')
    flats = []
    for section in sections:
        link = section.find('a')
        flat_id = link['href'].split('/')[-1].split('?')[0]

        if link.find_all('span')[1].text.endswith('$*'):
            price = link.find_all('span')[0].text + ' | ' + link.find_all('span')[1].text[:-1]
            address = link.find_all('span')[2]
        else:
            price = link.find_all('span')[0].text
            address = link.find_all('span')[1]

        description = link.find('p')
        img_link = None
        if link.find('img'):
            img_link = link.find('img')['src']

        flat_data = {
            'flat_id': flat_id,
            'link': link['href'],
            'price': price,
            'address': address.text,
            'description': description.text,
            'img_link': img_link
        }
        flats.append(flat_data)
    return flats


def get_flats():
    flats = parse_flats()
    if flats:
        new_flats = []
        db = Database()
        for flat in flats:
            if db.get(Flat, flat['flat_id']) is not None:
                continue
            new_flats.append(flat)
            if db.create(Flat, flat):
                print(f"Successfully added flat {flat['flat_id']}")
        return new_flats
