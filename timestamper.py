from PIL import Image, ExifTags
import cv2 as cv
import os
import glob

path = os.getcwd()

while True:
        if os.path.exists("./input") is True:
            break
        else:
            os.mkdir("./input")

while True:
        if os.path.exists("./output") is True:
            break
        else:
            os.mkdir("./output")

images = glob.glob("input/*")


for image in images:
    exif_img = Image.open(image)
    exif_data = { ExifTags.TAGS[k]: v for k, v in exif_img.getexif().items() if k in ExifTags.TAGS }
    datetime = exif_data['DateTime']
    

    img = cv.imread(image)
    img_name = image[len("input/") :]
    img_text = cv.putText(img, datetime, (10, 100), cv.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 255), 5)

    new_name = f"ts_{img_name}"
    cv.imwrite(os.path.join(f"{path}/output", new_name), img_text)
