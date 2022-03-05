from japanese_media_manager.scripts.scrape import scrape

def test_scrape():
    assert scrape(None) is None
