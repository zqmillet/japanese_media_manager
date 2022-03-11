import random
import hashlib
import typing
import requests

from .exceptions import TranslationException

class Translator:
    """
    百度的翻译模块.
    """

    def __init__(self, app_id: str, app_key: str):
        """
        :param app_id: 百度翻译服务的 APP ID.
        :param app_key: 百度翻译服务的 APP KEY.
        """
        self.app_id = app_id
        self.app_key = app_key
        self.url = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        self.successful_code = '52000'

    def translate(self, text: str, from_language: str = 'auto', to_language: str = 'zh') -> str:
        """
        将 :py:obj:`text` 翻译成目标语言.

        :param text: 待翻译的文本.
        :param from_language: 原始语言, 默认值为自动检测语言.
        :param to_language: 目标语言, 默认值为简体中文.
        """
        salt = random.randint(32768, 65536)
        sign = hashlib.md5(f'{self.app_id}{text}{salt}{self.app_key}'.encode('utf8')).hexdigest()
        payload: typing.Dict[str, typing.Union[str, int]] = {'appid': self.app_id, 'q': text, 'from': from_language, 'to': to_language, 'salt': salt, 'sign': sign}

        response = requests.post(self.url, params=payload, headers=self.headers).json()

        if not response.get('error_code', self.successful_code) == self.successful_code:
            raise TranslationException(f'code: {response["error_code"]}, {response["error_msg"]}')

        return '\n'.join(item['dst'] for item in response['trans_result'])
