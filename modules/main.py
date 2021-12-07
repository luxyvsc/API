from firebase_admin import firestore


class MainModule(object):
    def get_firestore_db():
        return firestore.client()