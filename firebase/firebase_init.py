import firebase_admin
from firebase_admin import credentials

# Use the service account key file from the firebase folder
cred = credentials.Certificate("firebase/junction-2024-firebase-adminsdk-nkyl9-fe3b8a0f78.json")
firebase_admin.initialize_app(cred)

print("Firebase initialized successfully!")