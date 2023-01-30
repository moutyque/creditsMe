import os
from os.path import exists

import cv2
from timecode import Timecode

video_path = '/home/qmouty/Downloads/Transfusion/Transfusion.2023.720p.WEBRip.x264.AAC-[YTS.MX].mp4'
credits_start_time = "01:40:37:00"


# TODO: solve issue with properties to get the frame count and being able to extract all picture from credits
def extract_frame(path, start, output="frames"):
    if not os.path.exists(path):
        print(f"{path} do not exist")
        return
    cap = cv2.VideoCapture(path)  # video_name is the video being called
    number_of_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # Need to iter until reach the end
    fps = cap.get(cv2.CAP_PROP_FPS)
    tc1 = Timecode(fps, start)
    while tc1.frames < number_of_frames:
        path = f'{output}/frame_{str(tc1.frames)}.jpg'
        cap.set(1, tc1.frames)  # Where frame_no is the frame you want
        ret, frame = cap.read()  # Read the frame
        if not exists(path):
            cv2.imwrite(f'{output}/frame_{str(tc1.frames)}.jpg', frame)
        tc1.frames = tc1.frames + int(fps)


if __name__ == '__main__':
    extract_frame(video_path, credits_start_time)
