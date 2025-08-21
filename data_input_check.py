# 데이터 삽입 및 조회
import sqlite3
import os

# === DB 경로 설정 ===
DB_PATH = r"C:\Users\82108\Desktop\my\work\certiapp_ver2\certification.db"

# === DB 및 테이블 자동 생성 ===
def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS certification (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            birth TEXT NOT NULL,
            certificate_no TEXT NOT NULL UNIQUE,
            method TEXT,
            level TEXT,
            issue_date TEXT,
            expiry_date TEXT
        )
        """)
        conn.commit()
    print("✅ DB와 certification 테이블 준비 완료")

# 초기화 실행
init_db()

# === 데이터베이스 연결 ===
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# === 데이터 삽입 ===
insert_ok = True
if insert_ok:
    cursor.execute("""
    INSERT INTO certification (name, birth, certificate_no, method, level, issue_date, expiry_date)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, ("Jang Hoon", "None", "00027-2025-00", "UT-PA", "2", "2025.08.29", "2030.08.29"))

# === certificate_no 로 삭제 ===
delete_ok = False  # True로 바꾸면 실행
if delete_ok:
    cursor.execute("""
    DELETE FROM certification WHERE certificate_no = ?
    """, ("00004-2025-00",))

# === 이름으로 삭제 ===
subdel_ok = False
if subdel_ok:
    cursor.execute("""
    DELETE FROM certification WHERE name = ?
    """, ("Park Hae Cheon",))

# 변경 저장
conn.commit()

# === 데이터 조회 ===
cursor.execute('SELECT * FROM certification')
rows = cursor.fetchall()
print("\n📜 현재 데이터:")
for row in rows:
    print(row)

# 연결 종료
conn.close()
