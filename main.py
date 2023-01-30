from os import walk

import img_analyzer
from img_analyzer import process
from video_reader import extract_frame

video_path = '/home/qmouty/Downloads/Transfusion/Transfusion.2023.720p.WEBRip.x264.AAC-[YTS.MX].mp4'
credits_start_time = "01:40:37:00"
output = "./frames"


def process():
    result = dict()
    # TODO optimize by concurrent frame saving + name extracting => Merge analyze at the end
    extract_frame(video_path, credits_start_time)
    for (dirpath, dirnames, files) in walk(output):
        for file in files:
            result = {**result, **img_analyzer.process(f"{dirpath}/{file}")}
    print(result)


if __name__ == '__main__':
    process()
