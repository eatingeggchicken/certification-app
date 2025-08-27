import sqlite3

DB_PATH = r"C:\Users\82108\Desktop\my\work\certiapp_ver2\certification.db"

new_row = ("Jeon, Dong Seok", "19820805", "00014-2025-00", "RI", "2", "2025.08.29", "2030.08.29")
insert_id = 33  # 여기에 넣고 싶다!

with sqlite3.connect(DB_PATH) as conn:
    cur = conn.cursor()

    # 1. id ≥ 33 인 행들 id를 +1씩 밀기 (뒤에서부터 업데이트해야 충돌 없음)
    cur.execute("SELECT id FROM certification WHERE id >= ? ORDER BY id DESC", (insert_id,))
    rows = cur.fetchall()
    for (rid,) in rows:
        cur.execute("UPDATE certification SET id = ? WHERE id = ?", (rid+1, rid))

    # 2. 새 데이터 삽입 (id를 직접 지정)
    cur.execute("""
        INSERT INTO certification (id, name, birth, certificate_no, method, level, issue_date, expiry_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (insert_id,) + new_row)

    conn.commit()
    print("✅ 33번에 새 데이터 삽입 완료, 이후 id는 전부 +1 밀림")

    # 확인
    cur.execute("SELECT * FROM certification ORDER BY id")
    for row in cur.fetchall():
        print(row)