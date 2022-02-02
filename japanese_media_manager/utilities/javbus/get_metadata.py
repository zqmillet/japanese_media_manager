import requests
import urllib
import http
import bs4

def get_metadata(number, proxies=None):
    proxies = proxies or {
        'http': None,
        'https': None,
    }

    url = 'https://www.javbus.com/{number}'.format(number=urllib.parse.quote(number))
    response = requests.get(url, proxies=proxies, verify=False)

    if not response.status_code == http.HTTPStatus.OK:
        return

    with open(f'testcases/utilities/javbus/data/{number.lower()}.html', 'w', encoding='utf8') as file:
        file.write(response.text)

    return parse(response.text)

def parse(html):
    soup = bs4.BeautifulSoup(html)
