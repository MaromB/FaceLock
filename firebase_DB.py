import base64
import cv2
import firebase_admin
import numpy as np
from PIL import Image
from firebase_admin import credentials, firestore
from imgbeddings import imgbeddings

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
                encoded_faces.append(rgb_img)
            return encoded_faces
        else:
            print("No images found for this user.")
            return []
    else:
        print("No document found for this user.")
        return []


def check_username_existence(username):
    user_ref = db.collection('Users').where('Username', '==', username).get()
    return len(user_ref) > 0


def taking_embeddings_from_db(username):
    vectors = db.collection("Embedding").where('Username', '==', username).get()
    return vectors


def embeddings_vector(image_of_face, username):
    # opening the image
    img = Image.fromarray(image_of_face)
    # loading the `imgbeddings`
    ibed = imgbeddings()
    # calculating the embeddings
    embedding = ibed.to_embeddings(img)
    embedding_flat = embedding.flatten().tolist()
    db.collection('Embedding').document(username).set({'embedding': embedding_flat})


class Database:
    def __init__(self, username, password, first_name, last_name, email):
        self.login_screen = None
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
    
    def login_into_system(self):
        list_of_embeddings_of_faces = taking_embeddings_from_db(self.login_screen.username_input.text())
        face_of_user = Image.fromarray(self.frame)
        # list_of_answers = face_recognition.api.compare_faces(list_of_faces, self.face_encodings, tolerance=0.6)
        return any(list_of_faces)
