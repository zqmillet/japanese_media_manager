import os
import datetime
import sqlalchemy
import sqlalchemy.orm
import pytest

from japanese_media_manager.utilities.models import Video
from japanese_media_manager.utilities.models import Star
from japanese_media_manager.utilities.models import Base

@pytest.fixture(name='file_path')
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
@pytest.mark.parametrize('length', [233, None])
def test_video_model(session, title, keywords, series, outline, director, length):
    video = Video(
        number='HAHA-233',
        title=title,
        keywords=keywords,
        release_date=datetime.datetime.today().date(),
        length=length,
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
