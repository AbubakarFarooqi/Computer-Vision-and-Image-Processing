from tkinter import Tk, Toplevel, Label, Button, Frame, PhotoImage, SOLID

class ModalWindow:
    def __init__(self, root_window):
        self.root_window = root_window
        self.modal_window = Toplevel(self.root_window)
        self.modal_window.title("Modal Dialog")

        # Add widgets to the modal window
        label = Label(self.modal_window, text="This is a modal dialog.")
        label.pack(padx=20, pady=20)

        # Add a close button to close the modal window
        close_button = Button(self.modal_window, text="Close", command=self.close_modal)
        close_button.pack(pady=10)

        self.modal_window.transient(self.root_window)
        self.modal_window.grab_set()
        self.root_window.wait_window(self.modal_window)

    def close_modal(self):
        self.modal_window.destroy()


class App:
    def __init__(self):
        self.root_window = Tk()
        self.screen_width, self.screen_height = self.get_screen_resolution()
        self.root_window.geometry(f"{self.screen_width}x{self.screen_height}")
        self.root_window.columnconfigure(0, weight=1)

        self.frame_header = Frame(self.root_window, padx=5, pady=5, bd=2)
        self.frame_header.grid(row=0, column=0, pady=20)

        # Load an image (replace 'path_to_icon.png' with the actual path to your image file)
        self.icon_camera = PhotoImage(file='camIcon.png')

        # Create a button with the image as the icon
        self.btn_camera = Button(self.frame_header, bd=0.5, image=self.icon_camera, command=self.open_modal)
        self.btn_camera.pack(side="left", padx=80, pady=10)

        self.frame_video_name = Frame(self.frame_header, padx=5, pady=5, bd=2, relief=SOLID)
        self.frame_video_name.pack(side="left")

        self.lbl_video_name = Label(self.frame_video_name, text="file", width=100)
        self.lbl_video_name.pack()

        # Browse Button
        browse_button = Button(self.frame_header, text="Browse", command=self.on_browse_clicked)
        browse_button.pack(side="left", padx=50)

        self.root_window.mainloop()

    def get_screen_resolution(self):
        root = Tk()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.destroy()
        return screen_width, screen_height

    def on_browse_clicked(self):
        print("Azan")

    def open_modal(self):
        ModalWindow(self.root_window)

if __name__ == "__main__":
    app = App()
