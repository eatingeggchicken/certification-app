#데이터 삽입 및 조회
import sqlite3

# 데이터베이스 연결
conn = sqlite3.connect('certification.db')
cursor = conn.cursor()

# 삽입
insert_ok = False
if insert_ok:
    cursor.execute('''
    INSERT INTO certification (name, birth, certificate_no, method, level, issue_date, expiry_date)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', ("Park, Jae Hwang", "811019", "00020-2025-00", "TO", "2", "2025.04.29", "2030.04.29"))


# 삭제          + 삭제하고 아래 행들을 위로 당겨야 나중에 추가되는걸 쓰기 편할듯
delete_ok = False #사용할때 True로 바꾸기
if delete_ok:
    cursor.execute('''
    DELETE FROM certification WHERE certificate_no = ?
    ''', ("00004-2025-00",)) # 비워져 있는 부분에 삭제할 데이터 CERTIFICATE_NO 해놓으면 됨
    
# 삭제 sub 데이터 관리하면서 쓸 것
subdel_ok = False
if subdel_ok:
    cursor.execute('''
    DELETE FROM certification WHERE name = ?
    ''', ("Park Hae Cheon",)) # 이름으로 삭제


# 저장
conn.commit()

# 데이터 조회
cursor.execute('SELECT * FROM certification')
rows = cursor.fetchall()
for row in rows:
    print(row)
    
# 연결 종료
conn.close()