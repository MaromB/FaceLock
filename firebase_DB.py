import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate('C:/Users/Administrator/Downloads/facelock.json')
firebase_admin.initialize_app(cred)
db = firestore.client()


def check_username_existence(username):
    user_ref = db.collection('Users').where('Username', '==', username).get()
    return len(user_ref) > 0


def register_user(username, password, first_name, last_name, email):
    if not check_username_existence(username):
        user_data = {
            'Username': username,
            'Password': password,  # should hash the password before storing.
            'FirstName': first_name,
            'LastName': last_name,
            'Email': email
        }
        db.collection('Users').document(username).set(user_data)
        return True, None
    else:
        return False, f"Username '{username}' already exists."
