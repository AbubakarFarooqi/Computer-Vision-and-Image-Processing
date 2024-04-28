import cv2
import face_recognition
import os
import winsound

class Webcam:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

    def read_frame(self):
        ret, frame = self.cap.read()
        if ret:
            return frame
        else:
            return None

    def release(self):
        self.cap.release()

class FaceRecognition:
    def __init__(self):
        self.known_encodings = []
        self.known_names = []

    # Function to play beep sound
    @staticmethod
    def play_beep():
        frequency = 2500  # Set frequency to 2500 Hz
        duration = 1000  # Set duration to 1000 ms (1 second)
        winsound.Beep(frequency, duration)

    # Function to recognize faces
    def recognize_faces(self, image):
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_image)
        face_encodings = face_recognition.face_encodings(rgb_image, face_locations)

        for face_location, face_encoding in zip(face_locations, face_encodings):
            top, right, bottom, left = face_location

            # Check if the face is recognized
            matches = face_recognition.compare_faces(self.known_encodings, face_encoding)
            name = "Intruder"  # Default to Intruder if not recognized

            if True in matches:
                first_match_index = matches.index(True)
                name = self.known_names[first_match_index]
            else:
                self.play_beep()  # Play beep sound for intruder

            # Draw a rectangle around the face and display the name
            cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(image, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    # Function to load known faces and names
    def load_known_faces(self):
        self.known_encodings = []
        self.known_names = []

        if not os.path.exists("dataset"):
            print("No dataset found.")
            return

        for name in os.listdir("dataset"):
            for file_name in os.listdir(os.path.join("dataset", name)):
                image_path = os.path.join("dataset", name, file_name)
                image = face_recognition.load_image_file(image_path)
                encoding = face_recognition.face_encodings(image)

                if len(encoding) > 0:
                    self.known_encodings.append(encoding[0])
                    self.known_names.append(name)
    def add_person(self,name):
    # Create a new directory for the person if it doesn't exist
        person_dir = "dataset/" + name
        if not os.path.exists(person_dir):
            os.makedirs(person_dir)

    # Use webcam to capture images
        cap = cv2.VideoCapture(0)
        count = 0

        while count < 5:  # Capture 5 images for training
            ret, frame = cap.read()
            if not ret:
                break

        # Convert the frame to RGB (since face_recognition uses RGB images)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Find all face locations and encodings in the frame
            face_locations = face_recognition.face_locations(rgb_frame)

        # Save only the first face detected in each frame
            if len(face_locations) > 0:
                top, right, bottom, left = face_locations[0]
                face_image = rgb_frame[top:bottom, left:right]
                cv2.imwrite(person_dir + "/" + str(count) + ".jpg", cv2.cvtColor(face_image, cv2.COLOR_RGB2BGR))
                count += 1
    
                # Display the image with rectangle around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

            cv2.imshow('frame', frame)
            cv2.waitKey(500)  # Pause for 500 milliseconds (0.5 seconds)

        cap.release()
        cv2.destroyAllWindows()
class UserInterface:
    def __init__(self):
        pass

    @staticmethod
    def display_menu():
        print("Menu:")
        print("1. Continue with face recognition")
        print("2. Add a new person")
        choice = input("Enter your choice: ")
        return choice

    @staticmethod
    def enter_name():
        return input("Enter the name of the person: ")

    @staticmethod
    def show_frame(frame):
        cv2.imshow('frame', frame)
        return cv2.waitKey(1)

    @staticmethod
    def close_windows():
        cv2.destroyAllWindows()

if __name__ == "__main__":
    webcam = Webcam()
    face_recognition_system = FaceRecognition()
    user_interface = UserInterface()

    face_recognition_system.load_known_faces()

    while True:
        choice = user_interface.display_menu()

        if choice == "1":
            while True:
                frame = webcam.read_frame()
                if frame is None:
                    break

                face_recognition_system.recognize_faces(frame)
                key = user_interface.show_frame(frame)
                if key & 0xFF == ord('q'):
                    break

        elif choice == "2":
            name = user_interface.enter_name()
            face_recognition_system.add_person(name)

    webcam.release()
    user_interface.close_windows()
