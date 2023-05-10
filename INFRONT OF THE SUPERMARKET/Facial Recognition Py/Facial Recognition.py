import face_recognition
import cv2
import numpy as np
import requests
import csv

channel_id = 2102276
api_key = "SEH46J6SXYACJX83"


known_face_names = []
known_customer_ID = []
known_face_encodings = []


def SendResultToThingspeak(customerID):
    try:
        url = f"https://api.thingspeak.com/update?api_key={api_key}&field1={customerID}"
        response = requests.post(url)
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


def CreateShoppingCartFile(name, customerID):
    try:
        with open(
            f"./../CODE/INSIDE THE SUPERMARKET/SP SHOPPING CART/{name}{customerID}.txt",
            "w",
        ) as file:
            ...
    except IOError as e:
        print(f"Error: {e}")


filepath = 1
try:
    with open("./INFRONT OF THE SUPERMARKET/USERS_DATABASE.csv", "r") as file:
        reader = csv.reader(file, delimiter=";")
        for line in reader:
            known_face_names.append(line[0])
            known_customer_ID.append(line[6])
            userimage = face_recognition.load_image_file(str(line[7]))
            known_face_encodings.append(face_recognition.face_encodings(userimage)[0])
except FileNotFoundError:
    print(
        "The file './INFRONT OF THE SUPERMARKET/USERS_DATABASE.csv' could not be found."
    )
except IndexError:
    print(
        "An index error occurred while reading './INFRONT OF THE SUPERMARKET/USERS_DATABASE.csv'."
    )
except Exception as e:
    print(
        f"An error occurred while reading './INFRONT OF THE SUPERMARKET/USERS_DATABASE.csv': {e}"
    )


face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

capture = cv2.VideoCapture(0)

while True:
    try:
        ret, frame = capture.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = np.ascontiguousarray(small_frame[:, :, ::-1])

        if process_this_frame:
            face_locations = face_recognition.face_locations(
                rgb_small_frame, model="cnn|hog"
            )
            face_encodings = face_recognition.face_encodings(
                rgb_small_frame, face_locations
            )
            face_names = []

            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(
                    known_face_encodings, face_encoding
                )
                name = "Unknown"
                customerID = "0"

                face_distances = face_recognition.face_distance(
                    known_face_encodings, face_encoding
                )
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                    customerID = known_customer_ID[best_match_index]

                face_names.append(name)

        process_this_frame = not process_this_frame

        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

            cv2.rectangle(
                frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED
            )
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(
                frame,
                name + customerID,
                (left + 4, bottom - 4),
                font,
                0.5,
                (0, 0, 255),
                2,
            )
            SendResultToThingspeak(customerID)
            CreateShoppingCartFile(name, customerID)

        cv2.imshow("Image", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


capture.release()
cv2.destroyAllWindows()
