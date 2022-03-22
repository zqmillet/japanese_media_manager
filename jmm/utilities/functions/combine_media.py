from typing import List
from ffmpeg import concat
from ffmpeg import input as input_media

def combine_media(input_files: List[str], output_file: str) -> None:
    import pdb; pdb.set_trace()
    concat(*map(input_media, input_files)).output(output_file).run()
