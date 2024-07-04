import cv2
# import face_recognition
from firebase_DB import db


class imageCapture:
    def __init__(self):
        self.db = db

    def capture_image(self):
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()
        cv2.destroyAllWindows()
        return frame

    def register_user(self, username):
        frame = self.capture_image()
        face_encodings = face_recognition.face_encodings(frame)

        if face_encodings:
            face_encoding = face_encodings[0]
            user_data = {
                'username': username,
                'face_encoding': face_encoding.tolist()
            }

            db.collection('users').document(username).set(user_data)
            print(f'User {username} registered successfully.')
        else:
            print('No face detected. Please try again.')

    def authenticate_user(self):
        frame = self.capture_image()
        face_encodings = face_recognition.face_encodings(frame)

        if face_encodings:
            face_encoding = face_encodings[0]
            users = db.collection('users').stream()
            for user in users:
                user_data = user.to_dict()
                stored_face_encoding = user_data['face_encoding']

                matches = face_recognition.compare_faces([stored_face_encoding], face_encoding)
                if True in matches:
                    print(f'User authenticated as {user_data["username"]}')
                    return user_data["username"]
            print('Authentication failed.')
        else:
            print('No face detected. Please try again.')

