from japanese_media_manager.utilities.crawlers import AirAvCrawler

def test_get_fields():
    fields = AirAvCrawler.get_fields()
    print(fields)
