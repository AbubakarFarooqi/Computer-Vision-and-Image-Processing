from tkinter import *
from tkinter import filedialog,ttk,simpledialog
import cv2 as cv
from PIL import Image, ImageTk
import time
import numpy as np



# http://50.231.121.221/axis-cgi/mjpg/video.cgi
#video file
video_capture = None
isPaused = True
fps = None
speed = 1
def get_photo_from_frame(frame):
     # Convert the frame to RGB format
        # It is because PhotoImage use RGB format
        rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        # Resize frame to fit in video player
        resized_frame = cv.resize(rgb_frame, (1000, 400))
        # Convert the resized frame to a PhotoImage from numPy array
        # representing openCV frame to PhotoImage
        photo = ImageTk.PhotoImage(Image.fromarray(resized_frame))
        return photo
        # lblVideoFrame.config(image=photo)
        # Keeping reference of image to avoid garbage collection
        # lblVideoFrame.image = photo


def set_first_frame(capVideo):
    if(capVideo.isOpened()):
        global video_capture
        global fps
        video_capture = capVideo
        fps = video_capture.get(cv.CAP_PROP_FPS) 
        ret,frame = capVideo.read()
        photo =  get_photo_from_frame(frame)
        lblVideoFrame.config(image=photo)
        # Keeping reference of image to avoid garbage collection
        lblVideoFrame.image = photo
        print(capVideo.get(cv.CAP_PROP_FRAME_HEIGHT))
        return True
    else:
        return False


def on_Browse_Clicked():
    selected_video_path = filedialog.askopenfilename(title="Select a video", filetypes=[("Video files", "*.mp4;*.avi;*.mkv;*.mov;*.wmv")])
    capVideo =  cv.VideoCapture(selected_video_path)
    # capVideo =  cv.VideoCapture("http://50.231.121.221/axis-cgi/mjpg/video.cgi")
    if(set_first_frame(capVideo)):
        lblVideoName.config(text=selected_video_path)
        print("video opended")
    else:
        print("video not opened")
   





def open_modal():
    def open_primary_camera():
        capVideo =  cv.VideoCapture(0)
        if(set_first_frame(capVideo)):
            lblVideoName.config(text="Primary Camera")
            print("video opended")
            destroy_modal()
        else:
            print("video not opened")

    def open_secondary_camera():
        capVideo =  cv.VideoCapture(1)
        if(set_first_frame(capVideo)):
            lblVideoName.config(text="Secondary Camera")
            print("video opended")
            destroy_modal()

        else:
            print("video not opened")


    def open_ip_camera():
        ip_address = simpledialog.askstring("Input", "Enter IP of Camera:")
        capVideo =  cv.VideoCapture(ip_address)
        if(set_first_frame(capVideo)):
            lblVideoName.config(text=ip_address)
            print("video opended")
            destroy_modal()
        else:
            print("video not opened")
    def destroy_modal():
        modal_window.destroy()
    # Create a new Toplevel window (modal dialog)
    modal_window = Toplevel(rootWindow)
    modal_window.title("Select Camera")

    # Add widgets to the modal window
    btnPrimaryCam = Button(modal_window,text="Primary Camera",command=open_primary_camera)
    btnPrimaryCam.pack(pady=5)

    btnSecondaryCam = Button(modal_window,text="Secondary Camera",command=open_secondary_camera)
    btnSecondaryCam.pack(pady=5)

    btnIPCam = Button(modal_window,text="IP Camera",command=open_ip_camera)
    btnIPCam.pack(pady=5)

    # Add a close button to close the modal window
    close_button = Button(modal_window, text="Close", command=modal_window.destroy)
    close_button.pack(pady=10)
    
    modal_window.geometry("+{}+{}".format(
    rootWindow.winfo_screenwidth() // 2 -modal_window.winfo_reqwidth() // 2,
    rootWindow.winfo_screenheight() // 2 -modal_window.winfo_reqheight() // 2
    ))

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


def set_frame_color(frame):
    if(cbxColorVar.get() == "Color"):
        return frame
    elif (cbxColorVar.get() == "GrayScale"):
        frame = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
        return frame
    elif (cbxColorVar.get() == "B/W"):
        frame = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
        frame = cv.adaptiveThreshold(
        frame, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 11, 4
    )
        return frame
    elif cbxColorVar.get() == "RedChannel":
        z=np.zeros((frame.shape[0],frame.shape[1]))
        frame[:,:,0] = z
        frame[:,:,1] = z
        return frame
    elif cbxColorVar.get() == "BlueChannel":
        z=np.zeros((frame.shape[0],frame.shape[1]))
        frame[:,:,1] = z
        frame[:,:,2] = z
        return frame
    elif cbxColorVar.get() == "GreenChannel":
        z=np.zeros((frame.shape[0],frame.shape[1]))
        frame[:,:,0] = z
        frame[:,:,2] = z
        return frame
        
    

def play_video():
    global isPaused
    isPaused = False
    global video_capture
    # ret,frame = video_capture.read()
    # if(ret):
    #     photo = get_photo_from_frame(frame)
    #     lblVideoFrame.config(image=photo)
    #     lblVideoFrame.image = photo
    while(not isPaused):
        start_time = time.time()
        ret,frame = video_capture.read()

        if(not ret):
            video_capture.set(cv.CAP_PROP_POS_FRAMES, 0)
            break

        frame =  set_frame_color(frame)
        photo = get_photo_from_frame(frame)
        lblVideoFrame.config(image=photo)
        lblVideoFrame.image = photo
        rootWindow.update()

        # Calculate the time taken to process a frame
        elapsed_time = time.time() - start_time
        delay = max(0,1/(speed*fps) - elapsed_time) # Here i use max to avoid negative values
        time.sleep(delay)

def pause_video():
    global  isPaused 
    isPaused = True
    rootWindow.update()

def on_speed_change(event):
    global speed
    speed = int(cbxSpeedVar.get())

def on_Color_Change(event):
    global color
    if(cbxColorVar.get() == "GrayScale"):
        color = cv.COLOR_BGR2GRAY
    





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

lblVideoName = Label(frameVideoName,text="abc",width=100)
lblVideoName.pack()

# Browse Button
btnBrowse = Button(frameHeader,text="Browse",command=on_Browse_Clicked)
btnBrowse.pack(side="left",padx=50)



#Video Player

frameVideoPlayer = Frame(rootWindow,height=400,width=1000, padx=5, pady=5, bd=2, relief=SOLID)
frameVideoPlayer.grid(row=1,column=0)
# Set grid_propagate to False to maintain the specified size
frameVideoPlayer.pack_propagate(False)
lblVideoFrame = Label(frameVideoPlayer)
lblVideoFrame.pack()

#Video Options Panel

frameVideoOption = Frame(rootWindow,padx=5, pady=5, bd=2)
frameVideoOption.grid(row=2,column=0)

iconPlay = PhotoImage(file='playIcon.png')
iconPause = PhotoImage(file='pauseIcon.png')
btnPlay = Button(frameVideoOption,bd=0.5, image=iconPlay, command=play_video)
btnPause = Button(frameVideoOption,bd=0.5, image=iconPause, command=pause_video)
btnPlay.pack(side="left" , padx=5, pady=10)
btnPause.pack(side="left" , padx=20, pady=10)

# combobox for changing speed
cbxSpeedVar = StringVar()
cbxSpeed = ttk.Combobox(frameVideoOption,textvariable=cbxSpeedVar, values=["1", "2", "3"],state="readonly")
cbxSpeed.set("1")  # Set the default text
# Bind the on_dropdown_change function to the <<ComboboxSelected>> event this function will be called when cbx value changes
cbxSpeed.bind("<<ComboboxSelected>>", on_speed_change)
cbxSpeed.pack(side=LEFT,padx=20)

# Combobox for changign colors

cbxColorVar = StringVar()
cbxColor = ttk.Combobox(frameVideoOption,textvariable=cbxColorVar, values=["Color","GrayScale", "B/W", "RedChannel","GreenChannel","BlueChannel"],state="readonly")
cbxColor.set("Color")  # Set the default text
# Bind the on_dropdown_change function to the <<ComboboxSelected>> event this function will be called when cbx value changes
# cbxColor.bind("<<ComboboxSelected>>", on_Color_Change)
cbxColor.pack(side=LEFT,padx=20)


# Running Program
rootWindow.mainloop()
