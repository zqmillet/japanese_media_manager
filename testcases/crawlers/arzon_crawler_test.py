import datetime
import pytest

from japanese_media_manager.crawlers import ArzonCrawler

@pytest.mark.parametrize(
    'number, title, outline, stars, series, studio, director, length, release_date', [
        (
            'STAR-325',
            '美人潜入捜査官 羽田あい',
            '黒のラバースーツを身に纏い、闇の組織と立ち向かう潜入捜査官・あいが敵に捕らわれてしまった！鎖で繋がれた連続イカセで潮が爆噴射状態！脈打つ塊を淫汁であふれるマ○コにぶち込まれ大量の連続中出し！',
            [{'name': '羽田あい', 'avatar_url': 'https://img.arzon.jp/image/3/50/50788S.jpg'}],
            'ＳＯＤｓｔａｒ',
            'ＳＯＤクリエイト（ソフトオンデマンド）',
            '本田教仁',
            120,
            '2011-12-08',
        ),
        (
            'SSIS-274',
            '【セクシースイーツ】今ここで喘ぎ声出したらイケナイでしょう？ お姉さんがベロキスでお口チャックしたままこっそりSEXシテあげる 星宮一花',
            '計算高いエッチな嫁の姉・一花さんが泊まりにやって来た。ファミレスやガレージ、妻と性交するベッドなど、いつでもどこでもお構いなしに求めて来る。僕は困惑するものの、あまりにも気持ち良過ぎて…。',
            [{'name': '星宮一花', 'avatar_url': 'https://img.arzon.jp/image/3/98/98758S.jpg'}],
            'Ｓ１　ＮＯ．１　ＳＴＹＬＥ',
            'Ｓ１（エスワン　ナンバーワンスタイル）',
            '真咲南朋',
            150,
            '2021-12-28'
        ),
        (
            'IDBD-809',
            '【セクシースイーツ】中年好きな文学美少女に身動きできない状態で8時間じっくりねっとり痴女られる総集編',
            '文系作品最高峰！超人気シリーズその豪華8時間ベストが登場！清楚で知的な美少女の中に隠された歪んだ性癖。'
            'そんな彼女達に辱められ服従し性奴隷にされる最高の悦び！目隠しされ拘束され身動きできない状態でねっちょり全身リップ。羞恥心を煽る囁き知的淫語！'
            '尿道から顔面に目がけて放たれるオシッコ！四つん這いにされアナルをベロベロ舐められながら辱め手コキ！女の子みたいな可愛い声出してどうされたんですか？',
            [
                {'name': '明里つむぎ', 'avatar_url': 'https://img.arzon.jp/image/3/94/94475S.jpg'},
                {'name': '相沢みなみ', 'avatar_url': 'https://img.arzon.jp/image/3/93/93460S.jpg'},
                {'name': '桃乃木かな', 'avatar_url': 'https://img.arzon.jp/image/3/90/90869S.jpg'},
                {'name': '桜空もも', 'avatar_url': 'https://img.arzon.jp/image/3/94/94633S.jpg'}
            ],
            'アイデアポケットBEST',
            'アイデアポケット',
            '',
            480,
            '2019-11-13'
        ),
        (
            'OFJE-220',
            '【セクシースイーツ】星宮一花 初ベスト S1デビュー1周年 最新11タイトル8時間スペシャル',
            '長身スレンダーBODYのお嬢様、星宮一花が奇跡のAV出演を果たしてから1年。今までに出演したすべての作品をまとめた初めてのベスト盤。'
            '綺麗な顔に汚い精子を浴びせられたり、細い腰が折れそうなほどエビ反りイキしたり、チンポに跨り我を忘れて腰を振る！星宮一花の1年分のSEXがすべて見られる最高傑作をお楽しみください！',
            [{'name': '星宮一花', 'avatar_url': 'https://img.arzon.jp/image/3/98/98758S.jpg'}],
            'Ｓ１　ＮＯ．１　ＳＴＹＬＥ',
            'Ｓ１（エスワン　ナンバーワンスタイル）',
            '',
            480,
            '2019-11-07',
        )
    ]
)
def test_arzon_metadata(number, title, outline, stars, series, studio, director, length, release_date, proxies):
    crawler = ArzonCrawler(proxies=proxies)
    metadata = crawler.get_metadata(number)

    assert metadata['fanart'] is None
    assert metadata['poster'] is None
    assert metadata['title'] == title
    assert metadata['number'] == number
    assert metadata['outline'] == outline
    assert metadata['stars'] == stars
    assert metadata['series'] == series
    assert metadata['studio'] == studio
    assert metadata['director'] == director
    assert metadata['length'] == length
    assert metadata['release_date'] == datetime.datetime.strptime(release_date, '%Y-%m-%d').date()

@pytest.mark.parametrize('number', ['XXX-250', 'SB-250'])
def test_arzon_metadata_with_nonexistent_number(number, proxies):
    crawler = ArzonCrawler(proxies=proxies)
    metadata = crawler.get_metadata(number)

    assert metadata['fanart'] is None
    assert metadata['poster'] is None
    assert metadata['title'] is None
    assert metadata['number'] == number
    assert metadata['outline'] is None
    assert metadata['series'] is None
    assert metadata['studio'] is None
    assert metadata['director'] is None
    assert metadata['length'] is None
    assert metadata['release_date'] is None
    assert not metadata['stars']
