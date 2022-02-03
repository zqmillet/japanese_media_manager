import re

def get_number(number):
    match = re.match(r'(?P<>\w+)[ -_\.](?P<>\d+)', number)
    import pdb; pdb.set_trace()
