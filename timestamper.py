from PIL import (
    Image as Img,
    ExifTags
)
import cv2 as cv
import os
from tkinter import (
    filedialog as fd,
    ttk,
    StringVar,
    Tk
)

# build window with frames
window = Tk()
window.title('Timestamper')
window.columnconfigure(0, weight=1)
window.rowconfigure(0, weight=1)
mainframe = ttk.Frame(window, padding='3 3 12 12')
mainframe.grid(column=0, row=0, sticky=(N, W, E, S)) # type: ignore

# file browse and open
def openfile():
    global images
    images = fd.askopenfilenames()
images = ()
open_button = ttk.Button(mainframe, text='OPEN', command=openfile).grid(column=2, row=5)

# text entry
street = StringVar()
city = StringVar()
state = StringVar()
zip = StringVar()
street_ent = ttk.Entry(mainframe, textvariable=street)
street_ent.grid(column=1, row=1)
city_ent = ttk.Entry(mainframe, textvariable=city)
city_ent.grid(column=1, row=2)
state_ent = ttk.Entry(mainframe, textvariable=state)
state_ent.grid(column=1, row=3)
zip_ent = ttk.Entry(mainframe, textvariable=zip)
zip_ent.grid(column=1, row=4)

# labels
ttk.Label(mainframe, text='Street').grid(column=2, row=1, sticky=W)
ttk.Label(mainframe, text='City').grid(column=2, row=2, sticky=W)
ttk.Label(mainframe, text='State').grid(column=2, row=3, sticky=W)
ttk.Label(mainframe, text='ZIP').grid(column=2, row=4, sticky=W)

# save function
def save():
    path = fd.askdirectory()
    for image in images:
        exif_img = Img.open(image)
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
        cv.imwrite(os.path.join(f"{path}/", new_name), img_text) #type: ignore

# process action button
save_button = ttk.Button(mainframe, text='SAVE', command=save).grid(column=3, row=5)

street_ent.focus()
window.mainloop()