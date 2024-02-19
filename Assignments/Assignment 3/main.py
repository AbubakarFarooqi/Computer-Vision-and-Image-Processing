from tkinter import *
from tkinter import filedialog,ttk,simpledialog
import cv2 as cv

selected_image = None



def selection_changed(event):
    selected_option = combo_box.get()
    print("Selected option:", selected_option)

def on_Apply_Clicked():
    print("Azan")


def get_screen_resolution():
    root = Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.destroy()
    return screen_width, screen_height


def on_Browse_Clicked():
    global inputImage
    selected_image_path = filedialog.askopenfilename(title="Select a video", filetypes=[("Video files", "*.jpg;*.png;*.jpeg;")])
    image =  cv.imread(selected_image_path)

    if((image is not None)):
        inputImage = image
        lblImagePath.config(text=selected_image_path)
        print("image opended")
    else:
        print("image not opened")
   




# main window
global root
global inputImage
global outputImage
root = Tk()
screen_width, screen_height = get_screen_resolution()
root.geometry(f"{screen_width}x{screen_height}")
# root.columnconfigure(0, weight=1)  # column 0 of any row uses any available space
# root.rowconfigure(0, weight=1)     # row 0 uses any available space


# root.columnconfigure(0, weight=1)  # column 0 uses any available space
# root.rowconfigure(0, weight=0)     # row 0 doesn't expand
# root.rowconfigure(1, weight=1)     # row 1 can expand vertically





# Container for image name and browse Button

frameHeader = Frame(root,padx=5, pady=5, bd=2)
frameHeader.pack(pady=20)


# Label That display Image name
frameImageName = Frame(frameHeader, padx=5, pady=5, bd=2, relief=SOLID)
frameImageName.pack(side="left")

lblImagePath = Label(frameImageName,text="Image Path",width=100)
lblImagePath.pack(side=LEFT)


# Adding widgets in frameHeader

btnBrowse = Button(frameHeader,bd=0.5,text="Browse", command=on_Browse_Clicked)
btnBrowse.pack(side=LEFT,padx=50)



#Frame for both images
frameImages = Frame(root,height=300,width=500, pady=5)
frameImages.pack()

#Frame to display input image

frameInputImage = Frame(frameImages,height=300,width=500, pady=5, bd=2, relief=SOLID)
frameInputImage.pack(side=LEFT,padx=50)
# Set grid_propagate to False to maintain the specified size
frameInputImage.pack_propagate(False)
lblInputImage = Label(frameInputImage)
lblInputImage.pack()




#Frame to display output image

frameOutputImage = Frame(frameImages,height=300,width=500, padx=5, pady=5, bd=2, relief=SOLID)
frameOutputImage.pack(side=LEFT,padx=50)
# Set grid_propagate to False to maintain the specified size
frameOutputImage.pack_propagate(False)
lblOutputImage = Label(frameOutputImage)
lblOutputImage.pack()

#Filer selection and application controls

frameFilterControls = Frame(root)
frameFilterControls.pack()
# Create a list of options
options = ["Log transformation", "Negative", "Gamma transformation", "Contrast","Intensity Level","Laplace"]

# Create a Combobox widget
combo_box = ttk.Combobox(frameFilterControls, values=options)
combo_box.current(0)
combo_box.pack(side=LEFT,pady=10)

# Bind the selection event to the function
combo_box.bind("<<ComboboxSelected>>", selection_changed)

#Apply filter button

btnApply = Button(frameFilterControls,bd=0.5,text="Apply", command=on_Apply_Clicked)
btnApply.pack(side=LEFT,padx=50)

root.mainloop()