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
insert_ok = False
if insert_ok:
    cursor.execute("""
    INSERT INTO certification (name, birth, certificate_no, method, level, issue_date, expiry_date)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, ("Jeon, Dong Seok", "19820805", "00014-2025-00", "RI", "2", "2025.08.29", "2030.08.29"))

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

# 데이터 수정 발전 코드
# === 데이터 삭제 (id 기준) ===
delete_id_ok = False  # True로 바꾸면 실행
delete_id_target = 46  # 삭제할 id

# === 데이터 수정 (id 기준) ===
update_id_ok = False   # True로 바꾸면 실행
update_id_target = 47  # 수정할 id

# 수정할 값 (필요한 것만 넣기)
update_values = {
    "birth": "19740527",
    # "expiry_date": "2031.12.31"
}

with sqlite3.connect(DB_PATH) as conn:
    cur = conn.cursor()

    # 삭제 실행
    if delete_id_ok:
        cur.execute("DELETE FROM certification WHERE id = ?", (delete_id_target,))
        print(f"🗑️ id={delete_id_target} 데이터 삭제 완료")

    # 수정 실행
    if update_id_ok:
        set_clause = ", ".join([f"{col} = ?" for col in update_values.keys()])
        values = list(update_values.values())
        values.append(update_id_target)
        sql = f"UPDATE certification SET {set_clause} WHERE id = ?"
        cur.execute(sql, values)
        print(f"✏️ id={update_id_target} 데이터 수정 완료 ({update_values})")



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
