class TranslationException(Exception):
    """
    翻译异常. 比如网络用塞, 或者被服务器限流时, 会抛出该异常.
    """
