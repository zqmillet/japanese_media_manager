from jmm.utilities.functions import combine_media

def test_combine_media():
    combine_media(
        input_files=[
            '/Volumes/DISK2/AV/DXHK-001/DXHK-001-CD1.avi',
            '/Volumes/DISK2/AV/DXHK-001/DXHK-001-CD2.avi',
        ],
        output_file='/Volumes/DISK2/AV/DXHK-001/DXHK-001.avi'
    )
