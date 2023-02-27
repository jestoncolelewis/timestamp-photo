from PIL import Image, ExifTags
import cv2 as cv
import os
import tkinter as tk
from tkinter import filedialog as fd

# build window with frames
window = tk.Tk()
window.title('Image Converter')
address_frame = tk.Frame(window)
s_frame = tk.Frame(address_frame)
c_frame = tk.Frame(address_frame)
st_frame = tk.Frame(address_frame)
z_frame = tk.Frame(address_frame)
button_frame = tk.Frame(window)

# file browse and open and save
def openfile():
    global images, path
    images = fd.askopenfilenames()
images = ()
open_button = tk.Button(button_frame, text='OPEN', command=openfile)

# text entry
s_label = tk.Label(s_frame, text='Street')
street = tk.Entry(s_frame)
c_label = tk.Label(c_frame, text='City')
city = tk.Entry(c_frame)
st_label = tk.Label(st_frame, text='State')
state = tk.Entry(st_frame)
z_label = tk.Label(z_frame, text='ZIP')
zip = tk.Entry(z_frame)

# process function
def process():
    path = fd.askdirectory()
    for image in images:
        exif_img = Image.open(image)
        exif_data = { ExifTags.TAGS[k]: v for k, v in exif_img.getexif().items() if k in ExifTags.TAGS }
        
        datetime = exif_data['DateTime']
        c_s_z = city.get() + ', ' + state.get() + ' ' + zip.get()  
        text = [datetime, street.get(), c_s_z]
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
process_button = tk.Button(button_frame, text='PROCESS', command=process)

s_label.pack(side='left')
street.pack(side='right')
c_label.pack(side='left')
city.pack(side='right')
st_label.pack(side='left')
state.pack(side='right')
z_label.pack(side='left')
zip.pack(side='right')

open_button.pack(side='left')
process_button.pack(side='right')

address_frame.pack()
s_frame.pack()
c_frame.pack()
st_frame.pack()
z_frame.pack()
button_frame.pack()

window.mainloop()