from urllib.parse import urlparse

def is_url(url: str) -> bool:
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:  # pylint: disable=broad-except
        return False
