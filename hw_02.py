import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from pprint import pprint
import json
from decimal import Decimal

ua = UserAgent()

# url = "https://books.toscrape.com"
# headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}
# session = requests.session()
# response = session.get(url=url + '/index.html', headers=headers, params=params)
# soup = BeautifulSoup(response.text, 'html.parser')
# books = soup.find_all('li', {"class": "col-xs-6"})

count = 1
all_books = list()
while True:
    url = f"https://books.toscrape.com"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}

    session = requests.session()

    response = session.get(url=url + f'/catalogue/page-{count}.html', headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    books = soup.find_all('li', {"class": "col-xs-6"})

    if count > 50:
        break

    for book in books:
        book_info = {}

        name_info = book.find('h3').findChildren()

        book_info['name'] = name_info[0].get('title')
        book_info['url'] = url + '/catalogue/' + name_info[0].get('href')

        price_info = book.find('p', {'class': 'price_color'})
        book_info['price'] = float(price_info.getText()[2:])

        response_1 = session.get(url=book_info['url'], headers=headers)
        soup = BeautifulSoup(response_1.text, 'html.parser')

        books_1 = soup.find_all('article', {"class": "product_page"})
        for chld_book in books_1:
            name_chld_book = chld_book.find('table', {'class': 'table'}).findChildren()
            book_info['Availability'] = int(name_chld_book[15].getText().split('\n')[2].split()[2][1:])

            book_info['Description'] = chld_book.find_all('p')[3].get_text(strip=True)

        all_books.append(book_info)

    print(f'Обработана {count} страница')
    count += 1
with open('books.json', 'w') as f:
    json.dump(all_books, f)

print(len(all_books))
