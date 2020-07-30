import os
import cv2

root_folder = "./dataset"

folders_path = os.listdir(root_folder)

target_size = (300, 238)
standard_size = (240,330)

# percorre todas as pastas no root folder
for folder in folders_path:
    root_path = os.path.join(root_folder,folder)
    files_path = os.listdir(root_path)
    for file_path in files_path:
        file_full_path = os.path.join(root_path, file_path)

        print("Cropping "+file_full_path)

        img = cv2.imread(file_full_path, cv2.IMREAD_COLOR)
        img_resized = cv2.resize(img, standard_size)
        crop_img = img_resized[38:170, 26:214]
        img_resized_final_v2_agora_vai = cv2.resize(crop_img, target_size)
        img_border = cv2.copyMakeBorder(img_resized_final_v2_agora_vai, 31, 31, 0, 0, cv2.BORDER_CONSTANT, value=(255, 255, 255))
        cv2.imwrite(file_full_path, img_border)
