import firebase_admin
from firebase_admin import credentials

# Use the service account key file from the firebase folder
cred = credentials.Certificate("firebase/serviceAccountKey.json")
firebase_admin.initialize_app(cred)

print("Firebase initialized successfully!")