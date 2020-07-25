import os
import cv2

folder_path = "./pokemonImages"
files_path = os.listdir(folder_path)

target_size = (300, 198)

for file_path in files_path:
    file_full_path = os.path.join(folder_path, file_path)

    img = cv2.imread(file_full_path, cv2.IMREAD_COLOR)
    img_resized = cv2.resize(img, target_size)
    img_border = cv2.copyMakeBorder(img_resized, 51, 51, 0, 0, cv2.BORDER_CONSTANT, value=(255, 255, 255))
    cv2.imwrite(file_full_path, img_border)
