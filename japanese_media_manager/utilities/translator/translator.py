import random
import hashlib
import requests

from .exceptions import TranslationException

class Translator:
    def __init__(self, app_id, app_key):
        self.app_id = app_id
        self.app_key = app_key
        self.url = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        self.successful_code = '52000'

    def translate(self, text, from_language='auto', to_language='zh'):
        salt = random.randint(32768, 65536)
        sign = hashlib.md5(f'{self.app_id}{text}{salt}{self.app_key}'.encode('utf8')).hexdigest()
        payload = {'appid': self.app_id, 'q': text, 'from': from_language, 'to': to_language, 'salt': salt, 'sign': sign}

        response = requests.post(self.url, params=payload, headers=self.headers).json()

        if not response.get('error_code', self.successful_code) == self.successful_code:
            raise TranslationException(f'code: {response["error_code"]}, {response["error_msg"]}')

        return '\n'.join(item['dst'] for item in response['trans_result'])
