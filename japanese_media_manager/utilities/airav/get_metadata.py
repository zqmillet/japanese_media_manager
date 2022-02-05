import requests
import bs4

def get_metadata(number, proxies=None):
    url = f'https://cn.airav.wiki/video/{number}'
    proxies = proxies or {'http': None, 'https': None}
    response = requests.get(url, proxies=proxies, verify=False)

    with open(f'./testcases/utilities/airav/data/{number.lower()}.html', 'w', encoding='utf8') as file:
        file.write(response.text)
    # return MetaData(response.json())

class MetaData:
    def __init__(self, html, base_url='https://cn.airav.wiki'):
        self.soup = bs4.BeautifulSoup(html, 'html.parser')
        self.base_url = base_url

    @property
    def outline(self):
        for tag in self.soup.find_all('h5', 'mb-4'):
            if not tag.text.strip() == '劇情':
                continue
            for item in tag.next_elements:
                if item.name == 'p':
                    return item.text.strip()
        return None

    @property
    def title(self):
        for tag in self.soup.find_all('p', 'mb-1'):
            return tag.text.strip()

    @property
    def keywords(self):
        result = []
        for tag in self.soup.find_all('div', 'tagBtnMargin'):
            for link in tag.find_all('a'):
                result.append(link.text.strip())
        return result

    @property
    def length(self):
        return None

    @property
    def stars(self):
        result = []
        for tag in self.soup.find_all('ul', 'videoAvstarList'):
            for link in tag.find_all('a'):
                result.append(
                    {
                        'name': link.text.strip(),
                        'avatar_url': None
                    }
                )
        return result
