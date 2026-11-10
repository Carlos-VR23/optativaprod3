# app/core/firebase.py
import os
import firebase_admin
from firebase_admin import credentials, firestore
from app.core.config import settings

def get_firestore_client():
    if settings.FIRESTORE_EMULATOR_HOST:
        os.environ["FIRESTORE_EMULATOR_HOST"] = settings.FIRESTORE_EMULATOR_HOST
    
    if not firebase_admin._apps:
        if settings.FIREBASE_CREDENTIALS_PATH:
            cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
            firebase_admin.initialize_app(cred, {
                "projectId": settings.FIREBASE_PROJECT_ID
            })
        else:
            firebase_admin.initialize_app(options={
                "projectId": settings.FIREBASE_PROJECT_ID
            })
            
    return firestore.Client(project=settings.FIREBASE_PROJECT_ID)

db = get_firestore_client()