from os.path import join
from os import makedirs
from shutil import move
from typing import Optional
from xml.etree.ElementTree import tostring
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import tostring
from xml.dom import minidom
from bs4 import BeautifulSoup

from jmm.utilities.metadata import Video
from jmm.utilities.media_finder import FileInformation
from jmm.utilities.translator import Translator
from jmm.utilities.translator import TranslationException

class FileManager:
    def __init__(self, destination_directory: str, mode: str, translator: Optional[Translator] = None):
        self.mode = mode
        self.destination_directory = destination_directory
        self.translator = translator

    def manager(self, file_information: FileInformation, video: Video) -> None:
        directory = join(self.destination_directory, video.number)
        media_file_name = f'{video.number}{file_information.file_path.suffix}'
        nfo_file_name = f'{video.number}.nfo'
        fanart_file_name = f'{video.number}-fanart.jpg'
        poster_file_name = f'{video.number}-poster.jpg'


        makedirs(directory, exist_ok=True)
        move(file_information.file_path, join(directory, media_file_name))

        with open(join(directory, nfo_file_name), 'w', encoding='utf8') as file:
            file.write(self.get_xml_string(video))

        video.fanart.save(join(directory, fanart_file_name))
        video.poster.save(join(directory, poster_file_name))
        return directory

    def translate(self, text: str) -> str:
        if not self.translator:
            return text

        try:
            return self.translator.translate(text)
        except TranslationException:
            return text

    def get_xml_string(self, video: Video) -> str:
        # movie = Element('media', attrib={'type': 'movie'})
        # SubElement(movie, 'title').text = video.title
        # SubElement(movie, 'description').text = self.translate(video.outline)
        # SubElement(movie, 'published').text = video.release_date.strftime('%Y-%m-%d') if video.release_date else None
        # genres = SubElement(movie, 'genres')
        # for keyword in video.keywords:
        #     SubElement(genres, 'genre').text = keyword

        # cast = SubElement(movie, 'cast')
        # for star in video.stars:
        #     SubElement(cast, 'name').text = star.name

        # SubElement(SubElement(movie, 'producers'), 'name').text = video.studio
        # SubElement(SubElement(movie, 'directors'), 'name').text = video.director


        movie = Element('movie')
        SubElement(movie, 'title').text = self.translate(video.title)
        SubElement(movie, 'set').text = None
        SubElement(movie, 'rating').text = str(0)
        SubElement(movie, 'studio').text = video.studio
        SubElement(movie, 'year').text = str(video.release_date.year) if video.release_date else None
        # SubElement(movie, 'originaltitle').text = video.title
        SubElement(movie, 'outline').text = video.outline
        SubElement(movie, 'plot').text = video.outline
        SubElement(movie, 'runtime').text = str(video.runtime) if video.runtime else None
        SubElement(movie, 'premiered').text = video.release_date.strftime('%Y-%m-%d') if video.release_date else None
        SubElement(movie, 'release').text = video.release_date.strftime('%Y-%m-%d') if video.release_date else None
        SubElement(movie, 'maker').text = video.studio
        SubElement(movie, 'director').text = video.director
        SubElement(movie, 'num').text = video.number

        for keyword in video.keywords:
            SubElement(movie, 'tag').text = keyword

        for star in video.stars:
            actor = SubElement(movie, 'actor')
            SubElement(actor, 'name').text = star.name
            SubElement(actor, 'role').text = star.name
            SubElement(actor, 'thumb').text = 'https://image.tmdb.org/t/p/h632/6ci3wf6oecjz875QRwryOsapW0Y.jpg'
            SubElement(actor, 'profile').text = 'https://www.themoviedb.org/person/24047'
            SubElement(actor, 'tmdbid').text = str(24047)

        return minidom.parseString(tostring(movie, 'UTF-8')).toprettyxml(indent=' '*2)
