from tkinter import *
from tkinter import filedialog,ttk,simpledialog
import cv2 as cv

selected_image = None


def get_screen_resolution():
    root = Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.destroy()
    return screen_width, screen_height


def on_Browse_Clicked():
    global selected_image
    selected_image_path = filedialog.askopenfilename(title="Select a video", filetypes=[("Video files", "*.jpg;*.png;*.jpeg;")])
    image =  cv.imread(selected_image_path)

    if(image):
        selected_image = image
        lblVideoName.config(text=selected_video_path)
        print("image opended")
    else:
        print("image not opened")
   




# main window
global root
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



#Frame to display input image

frameInputImage = Frame(root,height=400,width=500, padx=5, pady=5, bd=2, relief=SOLID)
frameInputImage.pack(side=LEFT)
# Set grid_propagate to False to maintain the specified size
frameInputImage.pack_propagate(False)
lblInputImage = Label(frameInputImage)
lblInputImage.pack()




#Frame to display output image

frameOutputImage = Frame(root,height=400,width=500, padx=5, pady=5, bd=2, relief=SOLID)
frameOutputImage.pack(side=LEFT)
# Set grid_propagate to False to maintain the specified size
frameOutputImage.pack_propagate(False)
lblOutputImage = Label(frameOutputImage)
lblOutputImage.pack()



root.mainloop()