from tkinter import *


def onBrowseClicked():
    # lblVideoName.configure(text=fileName)
    print("Azan")

def open_modal():
    # Create a new Toplevel window (modal dialog)
    modal_window = Toplevel(rootWindow)
    modal_window.title("Modal Dialog")

    # Add widgets to the modal window
    label = Label(modal_window, text="This is a modal dialog.")
    label.pack(padx=20, pady=20)

    # Add a close button to close the modal window
    close_button = Button(modal_window, text="Close", command=modal_window.destroy)
    close_button.pack(pady=10)

    modal_window.transient(rootWindow)
    modal_window.grab_set()
    rootWindow.wait_window(modal_window)
    # rootWindow.grab_release()


def get_screen_resolution():
    root = Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.destroy()
    return screen_width, screen_height


fileName = "file"

#initializaing root window
global rootWindow
rootWindow = Tk()
screen_width, screen_height = get_screen_resolution()
rootWindow.geometry(f"{screen_width}x{screen_height}")
rootWindow.columnconfigure(0, weight=1) #col 0 use any available space

# Container for video name and browse Button
frameHeader = Frame(rootWindow,padx=5, pady=5, bd=2)
frameHeader.grid(row=0,column=0,pady=20)


#Camera Icon Button

# Load an image (replace 'path_to_icon.png' with the actual path to your image file)
iconCamera = PhotoImage(file='camIcon.png')

# Create a button with the image as the icon
btnCamer = Button(frameHeader,bd=0.5, image=iconCamera, command=open_modal)
btnCamer.pack(side="left" , padx=80, pady=10)


# Label That display video name
frameVideoName = Frame(frameHeader, padx=5, pady=5, bd=2, relief=SOLID)
frameVideoName.pack(side="left")

lblVideoName = Label(frameVideoName,text=fileName,width=100)
lblVideoName.pack()

# Browse Button
browseButton = Button(frameHeader,text="Browse",command=onBrowseClicked)
browseButton.pack(side="left",padx=50)


# Running Program
rootWindow.mainloop()
