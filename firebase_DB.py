import base64
import cv2
import firebase_admin
import numpy as np
from PIL import Image
from firebase_admin import credentials, firestore
from imgbeddings import imgbeddings
from scipy.spatial.distance import cosine

cred = credentials.Certificate('C:/Users/Administrator/Downloads/facelock.json')
firebase_admin.initialize_app(cred)
db = firestore.client()


def check_username_existence(username):
    user_ref = db.collection('Users').where('Username', '==', username).get()
    return len(user_ref) > 0


def taking_embeddings_from_db(username):
    vectors = []
    doc_ref = db.collection("Embedding").document(username).collection('vectors').stream()

    for doc in doc_ref:
        data = doc.to_dict()
        if 'embedding' in data:
            embedding = data['embedding']
            vector = np.array(embedding)
            vectors.append(vector)

    return vectors


def embeddings_faces_to_vectors(images_of_face, username):
    for face in images_of_face:
        # opening the image
        img = Image.fromarray(face)
        # loading the `imgbeddings`
        ibed = imgbeddings()
        # calculating the embeddings
        embedding = ibed.to_embeddings(img)
        embedding_flat = embedding.flatten().tolist()
        db.collection('Embedding').document(username).set({'embedding': embedding_flat})
        user_ref = db.collection('Embedding').document(username)
        subcollection_ref = user_ref.collection('vectors')
        doc_id = len(subcollection_ref.get()) + 1
        subcollection_ref.document(str(doc_id)).set({'embedding': embedding_flat})


def compare_embeddings(embeddings_db, embedding_user):
    for i, embedding in enumerate(embeddings_db, start=1):
        if cosine(embedding, embedding_user) < 0.2:
            print(f'True {i}')
            return True
        print(f'False {i}')
    return False


class Database:
    def __init__(self, username, password=None, first_name=None, last_name=None, email=None):
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
    
    def login_into_system(self, frame):
        list_of_embeddings_of_faces = taking_embeddings_from_db(self.username)

        img = Image.fromarray(frame)
        ibed = imgbeddings()
        embedding_user = ibed.to_embeddings(img)
        embedding_flat_user = embedding_user.flatten().tolist()
        answer = compare_embeddings(list_of_embeddings_of_faces, embedding_flat_user)

        return answer
