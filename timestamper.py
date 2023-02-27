from PIL import Image, ExifTags
import cv2 as cv
import os
import tkinter as tk
from tkinter import filedialog as fd

# build window
window = tk.Tk()
window.title('Image Converter')
window.resizable(False, False)
window.geometry('300x200')

# file browse and open and save
def openfile():
    global images, path
    images = fd.askopenfilenames()
images = ()
open_button = tk.Button(window, text='OPEN', command=openfile)
open_button.pack()

def process():
    path = fd.askdirectory()
    for image in images:
        exif_img = Image.open(image)
        exif_data = { ExifTags.TAGS[k]: v for k, v in exif_img.getexif().items() if k in ExifTags.TAGS }
        datetime = exif_data['DateTime']
        

        img = cv.imread(image)
        img_name = image[:]
        name_l = image.rfind('/')
        img_name = image[name_l+1:]
        img_text = cv.putText(img, datetime, (10, 100), cv.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 255), 5)

        new_name = f"ts_{img_name}"
        cv.imwrite(os.path.join(f"{path}/", new_name), img_text)

# process action button
process_button = tk.Button(text='PROCESS', command=process)
process_button.pack()

window.mainloop()