import pytest

from japanese_media_manager.utilities.crawlers.do_nothing import do_nothing

def function_1():
    return None

def function_2():
    return 1 + 2

def function_3():  # pylint: disable = useless-return
    print([])
    return None

def function_4():  # pylint: disable = useless-return
    for index in [1, 2, 3]:
        print(index)
    return None

def function_5(number):
    if number == 3:
        return None
    return None

def function_6():
    return

def function_7():
    '''
    do_nothing
    '''

def function_8():
    '''
    do_nothing
    '''
    return

def function_9():
    pass

@pytest.mark.parametrize(
    'function, result', [
        (function_1, True),
        (function_2, False),
        (function_3, False),
        (function_4, False),
        (function_5, False),
        (function_6, True),
        (function_7, True),
        (function_8, True),
        (function_9, True),
    ]
)
def test_only_return_none(function, result):
    assert do_nothing(function=function) == result
