# 데이터 삽입 및 조회 (통합 리팩토링)
import sqlite3
import os
import shutil
from datetime import datetime

# === DB 경로 설정(절대경로 고정) ===
DB_PATH = r"C:\Users\82108\Desktop\my\work\certiapp_ver2\certification.db"

# === 유틸: 경로/연결 정보 출력 ===
def print_db_info():
    print("🔗 DB_PATH as set:", DB_PATH)
    print("📁 Absolute path:", os.path.abspath(DB_PATH))
    exists = os.path.exists(DB_PATH)
    size = os.path.getsize(DB_PATH) if exists else 0
    print("📦 Exists?", exists, " Size:", size)

# === 안전: 실행 전 백업 ===
def backup_db():
    if os.path.exists(DB_PATH):
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        bak = DB_PATH.replace(".db", f"_{ts}.bak.db")
        shutil.copy2(DB_PATH, bak)
        print(f"🛟 백업 생성: {bak}")

# === DB 및 테이블 자동 생성 (스키마 변경 없음) ===
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

# === CRUD 함수들 ===
def insert_cert(name, birth, certificate_no, method, level, issue_date, expiry_date):
    """안전 삽입(즉시 커밋). 중복이면 에러 메세지 표시."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO certification
                (name, birth, certificate_no, method, level, issue_date, expiry_date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (name, birth, certificate_no, method, level, issue_date, expiry_date))
            print(f"✅ INSERT OK id={cur.lastrowid} | {name} / {certificate_no} / {method}")
    except sqlite3.IntegrityError as e:
        print("⚠️ INSERT 실패(무결성 위반/중복 가능):", e)

def delete_by_certificate_no(certificate_no):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM certification WHERE certificate_no = ?", (certificate_no,))
        print(f"🗑️ certificate_no={certificate_no} 삭제 완료 (rows={cur.rowcount})")

def delete_by_name(name):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM certification WHERE name = ?", (name,))
        print(f"🗑️ name={name} 삭제 완료 (rows={cur.rowcount})")

def delete_by_id(row_id):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM certification WHERE id = ?", (row_id,))
        print(f"🗑️ id={row_id} 삭제 완료 (rows={cur.rowcount})")

def update_by_id(row_id, **fields):
    if not fields:
        print("ℹ️ 업데이트할 필드가 없습니다.")
        return
    set_clause = ", ".join([f"{k} = ?" for k in fields.keys()])
    values = list(fields.values())
    values.append(row_id)
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        sql = f"UPDATE certification SET {set_clause} WHERE id = ?"
        cur.execute(sql, values)
        print(f"✏️ id={row_id} 데이터 수정 완료 ({fields}, rows={cur.rowcount})")

def show_row_by_certificate_no(certificate_no):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT id, name, birth, certificate_no, method, level, issue_date, expiry_date
            FROM certification WHERE certificate_no = ?
        """, (certificate_no,))
        rows = cur.fetchall()
        print(f"🔎 {certificate_no} rows:", rows)

def list_all():
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM certification")
        rows = cur.fetchall()
        print("\n📜 현재 데이터:")
        for row in rows:
            print(row)

# ======================
# ===== 실행 영역 =====
# ======================
if __name__ == "__main__":
    print_db_info()
    backup_db()       # 실행 전 백업(원치 않으면 주석 처리)
    init_db()

    # === 플래그 (당신 코드 스타일 유지) ===
    insert_ok   = True
    delete_ok   = False   # certificate_no 기준 삭제
    subdel_ok   = False    # name 기준 삭제
    delete_id_ok = False  # id 기준 삭제
    update_id_ok = False  # id 기준 수정

    # === 대상 값들 (원래 코드 값 그대로 둠) ===
    insert_record = {
        "name": "Oh, Ki Rok",
        "birth": "851214",
        "certificate_no": "00037-2025-00",
        "method": "UT-PA",
        "level": "2",
        "issue_date": "2025.08.01",
        "expiry_date": "2030.08.01",
    }

    delete_certificate_no_target = "000-2025-00"
    delete_name_target = "Kim, Dae Min"
    delete_id_target = 46

    update_id_target = 47
    update_values = {
        "birth": "19740527",
        # "expiry_date": "2031.12.31"
    }

    # === 사전 점검(선택) ===
    show_row_by_certificate_no(insert_record["certificate_no"])

    # === 삽입 ===
    if insert_ok:
        insert_cert(
            insert_record["name"],
            insert_record["birth"],
            insert_record["certificate_no"],
            insert_record["method"],
            insert_record["level"],
            insert_record["issue_date"],
            insert_record["expiry_date"],
        )

    # === certificate_no 로 삭제 ===
    if delete_ok:
        delete_by_certificate_no(delete_certificate_no_target)

    # === 이름으로 삭제 ===
    if subdel_ok:
        delete_by_name(delete_name_target)

    # === id 기준 삭제 ===
    if delete_id_ok:
        delete_by_id(delete_id_target)

    # === id 기준 수정 ===
    if update_id_ok:
        update_by_id(update_id_target, **update_values)

    # === 결과 확인 ===
    show_row_by_certificate_no(insert_record["certificate_no"])
    list_all()
