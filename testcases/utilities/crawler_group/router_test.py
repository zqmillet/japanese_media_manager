import datetime
import PIL
import pytest

from japanese_media_manager.utilities.crawler_group import Router
from japanese_media_manager.utilities.crawler_group import Rule
from japanese_media_manager.utilities.crawler_group import CrawlerGroup

@pytest.mark.parametrize(
    'number, metadata', [
        (
            'STAR-325',
            {
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
            'FC2-PPV-2698221',
            {
                'poster': None,
                'keywords': ['巨乳'],
                'title': 'FC2-PPV-2698221 独占販売1本のおまけ動画あり【無修正ｘ個人撮影】巨乳タレ乳、ビラビラ乳首マンコに経産婦のだらしない体が激エロ過ぎる美人妻再び！流出してしまった動画をネタにホテルに連れ込んで、巨乳もみほぐし♪',
                'release_date': datetime.date(2022, 3, 4),
                'length': 69,
                'number': 'FC2-PPV-2698221',
                'director': None,
                'series': 'Kerberos',
                'studio': 'FC2-PPV',
                'stars': [],
                'outline': None
            }
        ),
    ]
)
def test_router(javbus, javdb, airav, avsox, logger, number, metadata):
    rule_1 = Rule(r'\w+-\d+', CrawlerGroup([javbus, javdb, airav], logger=logger))
    rule_2 = Rule(r'.*', CrawlerGroup([avsox, javdb], logger=logger))
    router = Router([rule_1, rule_2])

    _metadata = router.get_metadata(number)
    assert isinstance(_metadata.pop('fanart'), PIL.JpegImagePlugin.JpegImageFile)
    assert _metadata == metadata
