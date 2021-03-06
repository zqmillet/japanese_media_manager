import os
import uuid
import datetime
import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.exc
import pytest

from jmm.utilities.models import Video
from jmm.utilities.models import Star
from jmm.utilities.models import Base

@pytest.fixture(name='file_path', scope='function')
def _file_path():
    file_path = './sqlite.db'
    yield file_path
    if os.path.isfile(file_path):
        os.remove(file_path)

@pytest.fixture(name='session')
def _session(file_path):
    engine = sqlalchemy.create_engine(f'sqlite:///{file_path}')
    session = sqlalchemy.orm.sessionmaker(bind=engine)()
    Base.metadata.create_all(bind=engine)
    yield session
    session.close()

@pytest.mark.parametrize('title', ['gouliguojiashengsiyi'])
@pytest.mark.parametrize('keywords', [['haha', 'hoho'], []])
@pytest.mark.parametrize('series', [None, 'xianggangjizhe'])
@pytest.mark.parametrize('outline', [None, 'weixiaodegongxian'])
@pytest.mark.parametrize('director', [None, 'zhangzhe'])
@pytest.mark.parametrize('runtime', [233, None])
def test_video_model(session, title, keywords, series, outline, director, runtime):
    video = Video(
        number='HAHA-233',
        title=title,
        keywords=keywords,
        release_date=datetime.datetime.today().date(),
        runtime=runtime,
        series=series,
        outline=outline,
        director=director,
    )

    star_1 = Star(name='mario', avatar=None)
    star_2 = Star(name='luigi', avatar=None)
    star_3 = Star(name='kinopio', avatar=None)
    star_4 = Star(name='kinopico', avatar=None)

    video.stars = [star_1, star_2]
    session.add(video)
    session.commit()

    assert session.query(Video).one() is video
    assert star_1 in session.query(Video).one().stars
    assert star_2 in session.query(Video).one().stars
    assert star_3 not in session.query(Video).one().stars
    assert star_4 not in session.query(Video).one().stars

    assert star_1.videos == [video]
    assert star_2.videos == [video]
    assert star_3.videos == []
    assert star_4.videos == []

    assert repr(star_1) == '<star mario>'
    assert repr(star_2) == '<star luigi>'
    assert repr(star_3) == '<star kinopio>'
    assert repr(star_4) == '<star kinopico>'
    assert repr(video) == '<video HAHA-233>'

@pytest.mark.parametrize('title', ['gouliguojiashengsiyi'])
@pytest.mark.parametrize('keywords', [['haha', 'hoho'], []])
@pytest.mark.parametrize('series', [None, 'xianggangjizhe'])
@pytest.mark.parametrize('outline', [None, 'weixiaodegongxian'])
@pytest.mark.parametrize('director', [None, 'zhangzhe'])
@pytest.mark.parametrize('runtime', [233, None])
def test_video_star_model(session, title, keywords, series, outline, director, runtime):
    name = str(uuid.uuid1())
    star = Star(name=name, avatar=None)
    video = Video(
        number='HAHA-233',
        title=title,
        keywords=keywords,
        release_date=datetime.datetime.today().date(),
        runtime=runtime,
        series=series,
        outline=outline,
        director=director,
        stars=[star]
    )

    session.add(video)
    session.commit()
    stars = session.query(Star).all()
    assert len(stars) == 1
    assert stars[0] is star
