import random
import hashlib
import requests

class Translator:
    def __init__(self, app_id, app_key):
        self.app_id = app_id
        self.app_key = app_key
        self.url = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    def translate(self, text, from_language='auto', to_language='zh'):
        salt = random.randint(32768, 65536)
        sign = hashlib.md5(f'{self.app_id}{text}{salt}{self.app_key}'.encode('utf8')).hexdigest()
        payload = {'appid': self.app_id, 'q': text, 'from': from_language, 'to': to_language, 'salt': salt, 'sign': sign}
        response = requests.post(self.url, params=payload, headers=self.headers)
        return '\n'.join(item['dst'] for item in response.json()['trans_result'])
