import cv2
import face_recognition
import os

# Function to recognize faces
def recognize_faces(image):
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_image)
    face_encodings = face_recognition.face_encodings(rgb_image, face_locations)

    for face_location, face_encoding in zip(face_locations, face_encodings):
        top, right, bottom, left = face_location

        # Check if the face is recognized
        matches = face_recognition.compare_faces(known_encodings, face_encoding)
        name = "Intruder"  # Default to Intruder if not recognized

        if True in matches:
            first_match_index = matches.index(True)
            name = known_names[first_match_index]
        if name == "Intruder":
            print("Intruder")
        # Draw a rectangle around the face and display the name
        cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(image, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

# Function to add new person
def add_person(name):
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

# Function to load known faces and names
def load_known_faces():
    global known_encodings, known_names

    known_encodings = []
    known_names = []

    if not os.path.exists("dataset"):
        print("No dataset found.")
        return

    for name in os.listdir("dataset"):
        for file_name in os.listdir(os.path.join("dataset", name)):
            image_path = os.path.join("dataset", name, file_name)
            image = face_recognition.load_image_file(image_path)
            encoding = face_recognition.face_encodings(image)

            if len(encoding) > 0:
                known_encodings.append(encoding[0])
                known_names.append(name)

def main():
    # Load known faces and names
    load_known_faces()

    # Display the menu
    print("Menu:")
    print("1. Continue with face recognition")
    print("2. Add a new person")
    choice = input("Enter your choice: ")

    if choice == "1":
        # Capture video from webcam
        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            recognize_faces(frame)

            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    elif choice == "2":
        name = input("Enter the name of the person: ")
        add_person(name)

if __name__ == "__main__":
    main()
