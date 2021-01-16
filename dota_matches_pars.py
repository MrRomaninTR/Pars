import requests
from bs4 import BeautifulSoup
import csv
import re
CSV = 'content.csv'
URL = 'https://www.dotabuff.com/heroes/played?date=month'


HEADERS = {
    'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
    }

def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS)
    return r

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('tr')
    content = []
    for item in items:
        content.append(
            {
                'hero':item.find('td', class_='cell-xlarge').get('data-value'), 
                'matches':item.find('td').get('data-value'),
                'pickrate':item.find('td').get('data-value'),
                'winrate':item.find('td').get('data-value'),
                'kda':item.find('td', class_='r-none-mobile').get('data-value')
                }
            )
    return content

def save_parsing(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Hero', 'Matches', 'Pick Rate', 'Win Rate', 'KDA']) 
        for item in items:
            writer.writerow([item['hero'], item['matches'], item['pickrate'], item['winrate'], item['kda']])
            


def parser():
    html = get_html(URL)
    if html.status_code == 200:
        content = []
        content.extend(get_content(html.text))
        save_parsing(content, CSV)
    else:
        print('Error!')

parser()







    