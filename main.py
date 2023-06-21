import requests
from bs4 import BeautifulSoup
import csv

CSV = 'cards.csv'
HOST = 'https://www.olx.ua'
URL = 'https://www.olx.ua/d/uk/nedvizhimost/kvartiry/prodazha-kvartir/smela/'
HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}

def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='css-1sw7q4x')
    cards = []

    for item in items:

        if item.find('h6', class_='css-16v5mdi er34gjf0') == None:
           continue

        cards.append(
            {
                'title':item.find('h6', class_='css-16v5mdi er34gjf0').get_text(),
                'link_product': HOST + item.find('a').get('href'),
                'price': item.find('div', class_='css-u2ayx9').find('p', class_='css-10b0gli').get_text()
            }
        )
    return cards

def save_doc(items, path):
    with open(path, 'w', newline='', encoding='utf8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Заголовок', 'Лінк', 'Ціна'])
        for item in items:
            writer.writerow([item['title'], item['link_product'], item['price']])
    

def parser():
    PAGENATION = input('Укажите количество страниц: ')
    PAGENATION = int(PAGENATION)
    html = get_html(URL)
    if html.status_code == 200:
        cards = []
        for page in range(1, PAGENATION+1):
            print(f'Парсим страницу: {page}')
            html = get_html(URL, params={'page': page})
            cards.extend(get_content(html.text))
            save_doc(cards, CSV) 
        pass
    else:
        print('Error')

parser()