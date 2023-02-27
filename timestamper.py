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

street = tk.Entry(window)
city = tk.Entry(window)
state = tk.Entry(window)
zip = tk.Entry(window)

# process function
def process():
    path = fd.askdirectory()
    for image in images:
        exif_img = Image.open(image)
        exif_data = { ExifTags.TAGS[k]: v for k, v in exif_img.getexif().items() if k in ExifTags.TAGS }
        datetime = exif_data['DateTime']
        
        text = [datetime, street.get(), city.get(), state.get(), zip.get()]
        y = 100

        img = cv.imread(image)
        img_name = image[:]
        name_l = image.rfind('/')
        img_name = image[name_l+1:]
        for i in text:
            img_text = cv.putText(img, i, (10, y), cv.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 255), 5)
            y += 105

        new_name = f"ts_{img_name}"
        cv.imwrite(os.path.join(f"{path}/", new_name), img_text)

# process action button
process_button = tk.Button(text='PROCESS', command=process)

street.pack()
city.pack()
state.pack()
zip.pack()
open_button.pack()
process_button.pack()

window.mainloop()