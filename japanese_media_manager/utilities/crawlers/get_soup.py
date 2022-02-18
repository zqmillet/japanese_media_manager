import bs4

def get_soup(html):
    return bs4.BeautifulSoup(html, 'html.parser')
