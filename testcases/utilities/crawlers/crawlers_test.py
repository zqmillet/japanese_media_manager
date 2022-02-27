import datetime
import PIL.JpegImagePlugin
import pytest

from japanese_media_manager.utilities.crawlers import Crawlers
from japanese_media_manager.utilities.crawlers import AirAvCrawler
from japanese_media_manager.utilities.crawlers import ArzonCrawler
from japanese_media_manager.utilities.crawlers import AvsoxCrawler
from japanese_media_manager.utilities.crawlers import JavBusCrawler
from japanese_media_manager.utilities.crawlers import JavdbCrawler

@pytest.fixture(name='airav', scope='session')
def _airav(proxies):
    return AirAvCrawler(proxies=proxies)

@pytest.fixture(name='arzon', scope='session')
def _arzon(proxies):
    return ArzonCrawler(proxies=proxies, interval=1)

@pytest.fixture(name='avsox', scope='session')
def _avsox(proxies):
    return AvsoxCrawler(proxies=proxies)

@pytest.fixture(name='javbus', scope='session')
def _javbus(proxies):
    return JavBusCrawler(proxies=proxies)

@pytest.fixture(name='javdb', scope='session')
def _javdb(proxies):
    return JavdbCrawler(proxies=proxies)

class Logger(list):
    def debug(self, message, *args):
        self.append(('debug', message % args))

    def info(self, message, *args):
        self.append(('info', message % args))

    def warning(self, message, *args):
        self.append(('warning', message % args))

    def error(self, message, *args):
        self.append(('error', message % args))

    def critical(self, message, *args):
        self.append(('critical', message % args))

@pytest.fixture(name='logger', scope='function')
def _logger():
    return Logger()

def test_crawlers_warning(logger, arzon, avsox, javbus):
    Crawlers([arzon], required_fields=['poster', 'stars', 'outline'], logger=logger)
    assert logger[0] == ('warning', "cannot get fields 'poster' by the 1 crawler(s)")
    assert logger[1] == ('info', 'crawlers grouped by <crawler ArzonCrawler> is ready')
    logger.clear()

    Crawlers([avsox, arzon], required_fields=['fanart', 'stars', 'outline'], logger=logger)
    assert logger[0] == ('info', 'crawlers grouped by <crawler AvsoxCrawler>, <crawler ArzonCrawler> is ready')
    logger.clear()

    Crawlers([avsox, arzon, javbus], required_fields=['fanart', 'stars', 'outline', 'poster'], logger=logger)
    assert logger[0] == ('warning', "cannot get fields 'poster' by the 3 crawler(s)")
    assert logger[1] == ('info', 'crawlers grouped by <crawler AvsoxCrawler>, <crawler ArzonCrawler>, <crawler JavBusCrawler> is ready')
    logger.clear()

@pytest.mark.parametrize(
    'number, metatada', [
        (
            'star-325', {
                'poster': None,
                'keywords': ['STAR-325', 'SODクリエイト', '美人潜入捜査官', 'DVD多士爐', '女檢察官', '潮吹', '偶像藝人', '單體作品', '中出'],
                'title': 'STAR-325 美人潜入捜査官 羽田あい',
                'release_date': datetime.date(2012, 1, 8),
                'length': 120,
                'number': 'STAR-325',
                'director': '本田教仁',
                'series': '美人潜入捜査官',
                'studio': 'SODクリエイト',
                'stars': [{'avatar_url': 'https://www.javbus.com/pics/actress/6xv_a.jpg', 'name': '羽田あい'}],
                'outline': '潛入黑暗組織的「羽田亞衣」，雖然登場很瀟灑，不過沒多久就被敵人抓住了！被鎖鍊綁住連續調教，潮吹就像爆炸班狂噴！不斷反覆的凌虐，反而讓她沈溺在當中…。'
            }
        ),
        (
            'ssni-201', {
                'poster': None,
                'keywords': ['SSNI-201', 'S1NO.1STYLE', '校服', '巨乳', '單體作品', 'DMM獨家', '深喉', '凌辱', '薄馬賽克', '高畫質'],
                'title': 'SSNI-201 全員悪人レ○プ学園 鈴木心春 「もう誰も信じられない…」純粋で真面目な生徒会長は同級生に犯され男性教師に凌辱レ○プされ女性教師にまで折檻責めされて-',
                'release_date': datetime.date(2018, 5, 3),
                'length': 140,
                'number':
                'SSNI-201',
                'director': '肉尊',
                'series': None,
                'studio': 'エスワンナンバーワンスタイル',
                'stars': [{'avatar_url': 'https://www.javbus.com/pics/actress/8yw_a.jpg', 'name': '鈴木心春'}],
                'outline': '學生會長鈴木心春發現會計簿中有奇怪的收據，正義感很強的她與男教師談這件事卻遭背叛。這學校裡的教師、同學、朋友都是惡人，沒人願意幫她。讓她在癡漢、剃毛、口爆，凌辱性交中墜落性愛地獄。'
            }
        ),
        (
            'hunta-007', {
                'poster': None,
                'keywords': ['HUNTA-007', 'Hunter（ソフトオンデマンド）', '多P', '企畫', '姐妹', '高畫質'],
                'title': 'HUNTA-007 ヘタ過ぎる妹の彼氏に姉の私が直接SEX指導！私の可愛い妹（JK）が初めて家に彼氏を連れて来た。彼氏が真面目そうな子で安心したけど…思春期だし、部屋で2人きりになったらHな事をするに決まっている…。心配',
                'release_date': datetime.date(2015, 5, 21),
                'length': 233,
                'number': 'HUNTA-007',
                'director': 'アマゾン円童',
                'series': None,
                'studio': 'Hunter',
                'stars': [
                    {'avatar_url': 'https://www.javbus.com/pics/actress/314_a.jpg', 'name': '南梨央奈'},
                    {'avatar_url': 'https://www.javbus.com/pics/actress/2wr_a.jpg', 'name': '春原未来'},
                    {'avatar_url': 'https://www.javbus.com/pics/actress/944_a.jpg', 'name': '水希杏'},
                    {'avatar_url': 'https://www.javbus.com/pics/actress/895_a.jpg', 'name': '篠宮ゆり'},
                    {'avatar_url': 'https://www.javbus.com/pics/actress/mg9_a.jpg', 'name': '青葉優香'},
                    {'avatar_url': 'https://www.javbus.com/pics/actress/n00_a.jpg', 'name': '白石悠'}
                ],
                'outline': '學生妹首次帶了男友回家來。想說一定在房間幹起來了！但我看了一下發現男友技巧真是超爛！只好進去用肉體來個3P大指導！'
            }
        ),
        (
            'rki-460', {
                'poster': None,
                'keywords': ['RKI-460', 'ROOKIE', '中出', '單體作品', 'DMM獨家', '口交', '美少女', '乳房', '女上位', '高畫質'],
                'title': 'RKI-460 世界で一番エロく見える椎名そらの生々しいフェラチオと気持ち良すぎるSEX',
                'release_date': datetime.date(2018, 3, 3),
                'length': 130,
                'number': 'RKI-460',
                'director': '真咲南朋',
                'series': None,
                'studio': 'ROOKIE',
                'stars': [{'avatar_url': 'https://www.javbus.com/pics/actress/p84_a.jpg', 'name': '椎名そら'}],
                'outline': '世界で一番エロく見えるライティングとアングルで見せる最高にカワイイ椎名そら！目の前で舐められているかのような臨場感MAXのフェラチオ！ピンク乳首で美乳の天使のおっぱい！プリッとした弾力のあるまん丸のお尻！キュッとしまった美マンコに思いっきり中出し！最高にきれいなフェラチオと最高に気持ちいいSEXでイッちゃう！'
            }
        )
    ]
)
def test_get_metadata(number, metatada, javbus, javdb, airav):
    crawlers = Crawlers([javbus, javdb, airav], required_fields=['poster', 'stars', 'outline'])
    _metatada = crawlers.get_metadata(number)

    assert isinstance(_metatada.pop('fanart'), PIL.JpegImagePlugin.JpegImageFile)
    assert _metatada == metatada
