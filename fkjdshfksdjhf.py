import requests
from bs4 import BeautifulSoup


def fetch_exchange_rates(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        value_element = soup.select_one('.other-bank-course-block-bottom .cours-active .semibold-text')
        if value_element:
            value = value_element.get_text(strip=True)
            print(value)  # Output: 12 805 so'm
    except Exception as e:
        print(f"Error parsing the data: {e}")

        soup.select_one(
            'body > div.page-container > div.page-container__body > div:nth-child(7) > div > div.inform-page > div.left-side > div.other-bank-course-block.row > div.other-bank-course-block-bottom.row > div.col-2.cours-active > span.semibold-text')


url = 'https://bank.uz/uz/'
fetch_exchange_rates(url)
