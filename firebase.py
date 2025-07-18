import firebase_admin
from firebase_admin import credentials, firestore

# Firebase 인증 및 앱 초기화
cred = credentials.Certificate("path/to/your/credentials.json")
firebase_admin.initialize_app(cred)

# Firestore 데이터베이스 연결
db = firestore.client()

# 데이터 삽입 예시
def add_certification(cert_id, name, birth):
    doc_ref = db.collection('certifications').document(cert_id)
    doc_ref.set({
        'name': name,
        'birth': birth
    })