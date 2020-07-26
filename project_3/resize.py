import os
import cv2
from math import floor, ceil

folder_path = "./pokescrap/pokescrap/spiders/images/pngs"
files_path = os.listdir(folder_path)

target_size = (300, 300)

for file_path in files_path:
    file_full_path = os.path.join(folder_path, file_path)

    img = cv2.imread(file_full_path, cv2.IMREAD_COLOR)
    height, width, _ = img.shape
    if width > height:
        ratio = 300 / width
        img_resized = cv2.resize(img, (300, int(ratio * height)), interpolation=cv2.INTER_NEAREST)
        img_border = cv2.copyMakeBorder(img_resized, floor((300-int(ratio*height))/2), ceil((300-int(ratio*height))/2),
                                     0, 0, cv2.BORDER_CONSTANT, value=(255, 255, 255))
        cv2.imwrite(file_full_path, img_border)
    else:
        ratio = 300 / height
        img_resized = cv2.resize(img, (int(ratio * width), 300), interpolation=cv2.INTER_NEAREST)
        img_border = cv2.copyMakeBorder(img_resized, 0, 0,  floor((300-int(ratio*width))/2), ceil((300-int(ratio*width))/2),
                                         cv2.BORDER_CONSTANT, value=(255, 255, 255))
        cv2.imwrite(file_full_path, img_border)