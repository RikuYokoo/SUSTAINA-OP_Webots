import os
import datetime
import cv2
import numpy as np

class ImageWriter:
    def __init__(self, image_path = 'images', is_segmented_image = False):
        self.is_segmented_image = is_segmented_image
        self.save_image_count = 0

        dt_now_str = datetime.datetime.now().strftime('%y%m%dT%H%M%S')
        self.save_image_dir_path = image_path + "/" + dt_now_str
        self.createFolder()
        print("ImageWriter: Save image to " + self.save_image_dir_path)

    def createFolder(self, folder_name = None):
        if folder_name is None:
            folder_name = self.save_image_dir_path
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        print("ImageWriter: Create folder " + folder_name)

    def saveImage(self, raw_image, segmented_image = None):
        print("ImageWriter: Save image")
        if self.is_segmented_image:
            if segmented_image is None:
                return False

        image_name = str(self.save_image_count).zfill(6)
        cv2.imwrite(self.save_image_dir_path + "/" + image_name + "_label.png", segmented_image)
        cv2.imwrite(self.save_image_dir_path + "/" + image_name + ".png", raw_image)

        self.save_image_count += 1
