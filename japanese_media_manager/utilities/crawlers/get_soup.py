from bs4 import BeautifulSoup

def get_soup(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, 'html.parser')
