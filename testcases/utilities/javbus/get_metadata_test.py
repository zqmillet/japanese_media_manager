import datetime
import pytest

from japanese_media_manager.utilities.javbus import MetaData


@pytest.mark.parametrize(
    'number, title, keywords, release_date, stars, director, series, studio, length', [
        (
            'STAR-325',
            'STAR-325 美人潜入捜査官 羽田あい',
            ['STAR-325', 'SODクリエイト', '美人潜入捜査官', 'DVD多士爐', '女檢察官', '潮吹', '偶像藝人', '單體作品', '中出'],
            '2012-01-08',
            [{'avatar_url': 'https://www.javbus.com/pics/actress/6xv_a.jpg', 'name': '羽田あい'}],
            '本田教仁',
            '美人潜入捜査官',
            'SODクリエイト',
            (120, '分鐘'),
        ),
        (
            'ABP-888',
            'ABP-888 伝説の超高級サロン 究極のM性感 秘密倶楽部 乙都さきのが責めて責めて責めまくる！！',
            ['ABP-888', 'ABSOLUTELY PERFECT', '高畫質', '顏射', '玩具', '男の潮吹き', '單體作品', 'M男'],
            '2019-08-16',
            [{'avatar_url': 'https://www.javbus.com/pics/actress/rwd_a.jpg', 'name': '乙都さきの'}],
            'プノンペン凌',
            None,
            'プレステージ',
            (150, '分鐘'),
        ),
        (
            'ABP-960',
            'ABP-960 美少女と、貸し切り温泉と、濃密性交と。 09 最旬Fカップ美少女を一泊貸し切り、山奥の温泉宿へ 涼森れむ',
            ['ABP-960', 'ABSOLUTELY PERFECT', '美少女と、貸し切り温泉と、濃密性交と。', '高畫質', '單體作品', '拘束', 'SM', '乳交', '玩具', '巨乳'],
            '2020-03-20',
            [{'avatar_url': 'https://www.javbus.com/pics/actress/uly_a.jpg', 'name': '涼森れむ'}],
            None,
            '美少女と、貸し切り温泉と、濃密性交と。',
            'プレステージ',
            (133, '分鐘'),
        ),
        (
            'MMNT-010',
            'MMNT-010 派手そうに見えるけど実は人見知り… SEX偏差値MAXギャルがAvdebut 寺田ここの',
            ['MMNT-010', 'million mint（ミリオンミント）', 'DMM獨家', '單體作品', '多P', '首次亮相', '巨乳', '乳房', '潮吹'],
            '2021-08-07',
            [{'avatar_url': 'https://www.javbus.com/pics/actress/xnm_a.jpg', 'name': '寺田ここの'}],
            '馨',
            None,
            'ケイ・エム・プロデュース',
            (135, '分鐘'),
        ),
        (
            'ipx-292',
            'IPX-292 巨乳若妻は元彼ダメ男に嫌なほどイカされて… 桜空もも',
            ['IPX-292', 'ティッシュ', '巨乳', '單體作品', 'DMM獨家', '苗條', '乳交', '新娘、年輕妻子', '數位馬賽克', '高畫質', '出軌'],
            '2019-04-07',
            [{'avatar_url': 'https://www.javbus.com/pics/actress/r62_a.jpg', 'name': '桜空もも'}],
            '朝霧浄',
            None,
            'アイデアポケット',
            (120, '分鐘'),
        ),
        (
            'CEMD-011',
            'CEMD-011 ち○ぽが壊れる5秒前！手加減をしない責めるフルコース痴女SEX 辻井ほのか',
            ['CEMD-011', 'セレブの友', '成熟的女人', '單體作品', 'DMM獨家', '巨乳', '口交', '花癡', '蕩婦'],
            '2021-05-22',
            [{'avatar_url': 'https://www.javbus.com/pics/actress/vfl_a.jpg', 'name': '辻井ほのか'}],
            None,
            None,
            'セレブの友',
            (139, '分鐘'),
        ),
        (
            'CJOD-278',
            'CJOD-278 アナル見せつけWデカ尻メンズエステ 可愛い子の卑猥なケツ穴を眺めて何度も射精したい 松本いちか あおいれな',
            ['CJOD-278', '痴女ヘブン', '高畫質', 'DMM獨家', '肛交', '中出', '美容院', '姐姐', '多P'],
            '2021-01-23',
            [
                {'avatar_url': 'https://www.javbus.com/pics/actress/vb3_a.jpg', 'name': '松本いちか'},
                {'avatar_url': 'https://www.javbus.com/pics/actress/pey_a.jpg', 'name': 'あおいれな'}
            ],
            'トレンディ山口',
            None,
            '痴女ヘブン',
            (160, '分鐘'),
        ),
        (
            '100221_001',
            '100221_001 濃厚な接吻と肉体の交わり 世良あさか',
            ['100221_001', '濃厚な接吻と肉体の交わり', '無套', '口交', '振動', '苗條', 'AV女優', '美臀', '巨乳', '69', '美乳', '舔陰', '1080p', '內射', '手淫', '60fps'],
            '2021-10-02',
            [{'avatar_url': 'https://www.javbus.com/imgs/actress/nowprinting.gif', 'name': '世良あさか'}],
            None,
            '濃厚な接吻と肉体の交わり',
            '一本道',
            (59, '分鐘'),
        ),
        (
            'AVSW-061',
            'AVSW-061 AIKAの世界 4時間BEST',
            ['AVSW-061', 'AVS', '○○の世界', '4小時以上作品', '高畫質', 'DMM獨家', '單體作品', '其他戀物癖', '女生', '女優ベスト・総集編'],
            '2021-10-16',
            [{'avatar_url': 'https://www.javbus.com/pics/actress/2t4_a.jpg', 'name': 'AIKA'}],
            None,
            '○○の世界',
            'AVS collector’s',
            (240, '分鐘'),
        )
    ]
)
def test_metadata(number, title, keywords, release_date, stars, director, series, studio, length):
    with open(f'testcases/utilities/javbus/data/{number.lower()}.html', 'r', encoding='utf8') as file:
        metadata = MetaData(file.read())

    assert metadata.title == title
    assert metadata.keywords == keywords
    assert metadata.release_date == datetime.datetime.strptime(release_date, '%Y-%m-%d').date()
    assert metadata.length == length
    assert metadata.stars == stars
    assert metadata.number == number.upper()
    assert metadata.director == director
    assert metadata.series == series
    assert metadata.studio == studio
