import os
import pathlib

def get_answer(text):
    while True:
        answer = input(text).lower() or 'y'
        if answer in ['y', 'n']:
            return answer == 'y'

def generate_configuration(file_path=os.path.join(pathlib.Path.home(), '.jmm.cfg')):
    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.config.yaml'), 'r', encoding='utf8') as file:
        configuration = file.read()

    if os.path.isfile(file_path) and not get_answer(f'file {file_path} exists, overwrite it? (Y/n) '):
        return

    with open(file_path, 'w', encoding='utf8') as file:
        file.write(configuration)

    print(f'configuration has been saved in file {file_path}')
