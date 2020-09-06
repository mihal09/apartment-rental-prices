import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_page(page_id):
    """ Returns a list of page addresses from the page with the given id
    :param page_id: id of parsed page
    :return: list of addresses(strings)
    """

    url = 'https://www.gumtree.pl/s-mieszkania-i-domy-do-wynajecia/wroclaw/page-{}/v1c9008l3200114p{}' \
        .format(page_id, page_id)

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    addresses = []
    for child in soup.select('.view > div > div:nth-child(1) > a:nth-child(1)'):
        addresses.append(child.get('href'))

    return addresses


def get_flat(address):
    """
    :param address: address got from function get_page()
    :return: dictionary representing the flat
    """

    output = {}
    url = 'https://www.gumtree.pl{}'.format(address)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    try:
        output['name'] = soup.select('.myAdTitle')[0].text
    except IndexError:
        output['name'] = None

    try:
        price = soup.select('div.price:nth-child(2) > span:nth-child(1) > span:nth-child(1)')[0].text
        price = int(price.replace(' zł', '').replace(u'\xa0', ''))
        output['price'] = price
    except:
        return None

    map_address = soup.select('.google-maps-link')[0].get('data-uri')
    lat, long = [float(x) for x in map_address.split('=')[-1].split(',')]
    output['lat'] = lat
    output['long'] = long

    for attribute in soup.select('.selMenu > li > div:nth-child(1)'):
        children = list(attribute.children)
        if len(children) != 2:
            continue
        attribute_type = children[0].text
        attribute_value = children[1].text

        if attribute_type == 'Liczba pokoi':
            try:
                output['rooms'] = int(attribute_value.split()[0])
            except:
                output['rooms'] = 1
        elif attribute_type == 'Wielkość (m2)':
            try:
                output['size'] = int(attribute_value)
            except:
                return None

    return output


def scrape_data():
    rows = []
    for i in range(1, 51):
        for flat in get_page(i):
            flat_data = get_flat(flat)
            if flat_data is not None:
                rows.append(flat_data)
        print("{}/50".format(i))
    return pd.DataFrame(rows)


if __name__ == '__main__':
    df = scrape_data()
    df.to_csv('flats.csv')
