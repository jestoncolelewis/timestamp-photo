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
    IntVar,
    Tk,
    Listbox
)

# file browse and open
def openfile():
    global images
    images = fd.askopenfilenames()
images = ()

# save function
def save():
    path = fd.askdirectory()
    errors = []
    evar = StringVar(value=errors) #type: ignore
    for image in images:
        try:
            exif_img = Img.open(image)
            exif_data = { ExifTags.TAGS[k]: v for k, v in exif_img.getexif().items() if k in ExifTags.TAGS }
            
            datetime = exif_data['DateTime']
            c_s_z = city.get() + ', ' + state.get() + ' ' + zip.get()  
            text = [datetime, street.get(), c_s_z]

            img = cv.imread(image)
            name_l = image.rfind('/')
            img_name = image[name_l+1:]

            h = img.shape[0]
            w = img.shape[1]

            x = 0
            y = 0
            if var.get() == 1: # top left
                x = 10
                y = 100
            if var.get() == 2: # top right
                x = 10 #TODO
                y = 100
            if var.get() == 3: # bottom left
                x = 10
                y = h - 230
            if var.get() == 4: # bottom right
                x = w - 10 #TODO
                y = h - 230
            
            for i in text:
                img_text = cv.putText(img, i, (x, y), cv.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 255), 5)
                y += 105

            new_name = f"ts_{img_name}"
            cv.imwrite(os.path.join(f"{path}/", new_name), img_text) #type: ignore
        except KeyError:
            # error display
            error_box = Listbox(errorframe, height=8, listvariable=evar)
            error_box.grid(column=4, row=1, sticky='N')
            name_l = image.rfind('/')
            img_name = image[name_l+1:]
            errors.append('No date/time data for {}'.format(img_name))
            evar.set(errors) #type: ignore

# build window with frames
window = Tk()
window.title('Timestamper')
window.columnconfigure(0, weight=1)
window.rowconfigure(0, weight=1)
mainframe = ttk.Frame(window, padding='3 3 12 12')
mainframe.grid(column=0, row=0)
locations = ttk.Frame(window)
locations.grid(column=2, row=0)
errorframe = ttk.Frame(window, padding='3 3 12 12')
errorframe.grid(column=6, row=0)

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

# locations
var = IntVar()
top_left = ttk.Radiobutton(locations, text='Top Left', variable=var, value=1)
top_left.grid(column=3, row=0, sticky='W')
top_right = ttk.Radiobutton(locations, text='Top Right', variable=var, value=2)
top_right.grid(column=4, row=0, sticky='W')
bottom_left = ttk.Radiobutton(locations, text='Bottom Left', variable=var, value=3)
bottom_left.grid(column=3, row=1, sticky='W')
bottom_right = ttk.Radiobutton(locations, text='Bottom Right', variable=var, value=4)
bottom_right.grid(column=4, row=1, sticky='W')

# labels
ttk.Label(mainframe, text='Street').grid(column=2, row=1, sticky='W')
ttk.Label(mainframe, text='City').grid(column=2, row=2, sticky='W')
ttk.Label(mainframe, text='State').grid(column=2, row=3, sticky='W')
ttk.Label(mainframe, text='ZIP').grid(column=2, row=4, sticky='W')

# buttons
open_button = ttk.Button(mainframe, text='OPEN', command=openfile).grid(column=2, row=7)
save_button = ttk.Button(mainframe, text='SAVE', command=save).grid(column=3, row=7)

street_ent.focus()
window.mainloop()