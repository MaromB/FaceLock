import base64
import cv2
import face_recognition
import firebase_admin
import numpy as np
from firebase_admin import credentials, firestore

cred = credentials.Certificate('C:/Users/Administrator/Downloads/facelock.json')
firebase_admin.initialize_app(cred)
db = firestore.client()


def get_encoded_faces_from_db(username):
    doc_ref = db.collection('Faces').document(username)
    doc = doc_ref.get()

    if doc.exists:
        images_base64 = doc.get('images')
        if images_base64:
            encoded_faces = []
            for image_base64 in images_base64:
                # Step 1: Decode the base64 string to binary data
                image_data = base64.b64decode(image_base64)
                # Step 2: Convert the binary data to a numpy array
                nparr = np.frombuffer(image_data, np.uint8)
                # Step 3: Decode the numpy array to an OpenCV image
                img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                # Step 4: Convert the image to RGB format
                rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                # Step 5: Extract face encodings
                face_encodings = face_recognition.face_encodings(rgb_img)
                if face_encodings:
                    encoded_faces.append(face_encodings)
            return encoded_faces
        else:
            print("No images found for this user.")
            return []
    else:
        print("No document found for this user.")
        return []


def get_encoded_face(frame, debug_save_path="decoded_image.jpg"):
    cv2.imwrite('decoded_image.jpg', cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    image = face_recognition.load_image_file("decoded_image.jpg")

    # rgb_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    try:
        face_encodings = face_recognition.face_encodings(image)[0]
        if face_encodings:
            return face_encodings[0]
        else:
            print("No faces found in the image.")
            return None
    except Exception as e:
            print(f"Error in face recognition: {e}")
            return None


def check_username_existence(username):
    user_ref = db.collection('Users').where('Username', '==', username).get()
    return len(user_ref) > 0


def taking_faces_from_db(username):
    faces = get_encoded_faces_from_db(username)
    return faces


class Database:
    def __init__(self, username, password, first_name, last_name, email):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    def register_user(self):
        if not check_username_existence(self.username):
            user_data = {
                'Username': self.username,
                'Password': self.password,  # should hash the password before storing.
                'FirstName': self.first_name,
                'LastName': self.last_name,
                'Email': self.email
            }
            db.collection('Users').document(self.username).set(user_data)
            return True, None
        else:
            return False, f"Username '{self.username}' already exists."

    def save_images_in_db(self, images):
        encoded_images = [base64.b64encode(cv2.imencode('.jpg', img)[1]).decode('utf-8') for img in images]
        db.collection('Faces').document(self.username).set({'images': encoded_images})

