import firebase_admin
from firebase_admin import credentials, auth

# Initialize the Firebase Admin SDK with the service account key
cred = credentials.Certificate("path/to/your/serviceAccountKey.json")
firebase_admin.initialize_app(cred)
