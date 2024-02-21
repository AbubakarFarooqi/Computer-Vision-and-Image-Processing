from tkinter import *
from tkinter import filedialog,ttk,simpledialog
import cv2 as cv
import numpy as np
import tkinter as tk
from PIL import ImageTk, Image


selected_image = None

def log_transformation():
    # Apply the logarithmic transformation: s = c * log(1 + r)
    c = 255 / np.log(1 + np.max(inputImage))
    log_transformed_image = c * (np.log(inputImage + 1))
    # Convert to uint8
    log_transformed_image = np.uint8(log_transformed_image)
    return log_transformed_image
def negative():
    # Calculate the negative of the image
    return 255 - inputImage
def gamma_transformation():
    # Normalize the pixel values
    image_norm = inputImage / 255.0
    # Apply gamma correction
    corrected_image = np.power(image_norm, inputImage)
    # Convert back to the original range
    corrected_image = np.uint8(corrected_image * 255)
    return corrected_image

def contrast():
    # Define the alpha and beta values for contrast adjustment
    alpha = 1.5  # Contrast control (1.0 for no change)
    beta = 0    # Brightness control (0 for no change)

    # Apply the contrast adjustment
    return cv.convertScaleAbs(inputImage, alpha=alpha, beta=beta)
def intensity_level():
    # Apply histogram equalization
    return cv.equalizeHist(inputImage)
def laplace():
    # Apply Laplacian filter
    laplacian_filtered_image = cv   .Laplacian(inputImage, cv.CV_64F)

    # Convert back to uint8
    return cv.convertScaleAbs(laplacian_filtered_image)


def selection_changed(event):
    selected_option = combo_box.get()
    print("Selected option:", selected_option)


def on_Apply_Clicked():
    if(inputImage is None): return 

    selected_option = combo_box.get()
    image = NONE
    if selected_option == "Log transformation":
        image =  log_transformation()
    elif selected_option == "Negative":
        image =  negative()
    elif selected_option == "Gamma transformation":
        image =  gamma_transformation()
    elif selected_option == "Contrast":
        image =  contrast()
    elif selected_option == "Intensity Level":
        image =  intensity_level()
    elif selected_option == "Laplace":
        image =  laplace()

    image_pil = Image.fromarray(image)
    photo = ImageTk.PhotoImage(image_pil)
    lblOutputImage.image = photo
    lblOutputImage.config(image=photo)


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
        image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        image = cv.resize(image,(480,280))
        inputImage = image
        lblImagePath.config(text=selected_image_path)
        print("image opended")

        image_pil = Image.fromarray(inputImage)
        photo = ImageTk.PhotoImage(image_pil)
        lblInputImage.image = photo
        lblInputImage.config(image=photo)
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
combo_box = ttk.Combobox(frameFilterControls, values=options,state="readonly")
combo_box.current(0)
combo_box.pack(side=LEFT,pady=10)

# Bind the selection event to the function
combo_box.bind("<<ComboboxSelected>>", selection_changed)

#Apply filter button

btnApply = Button(frameFilterControls,bd=0.5,text="Apply", command=on_Apply_Clicked)
btnApply.pack(side=LEFT,padx=50)

root.mainloop()