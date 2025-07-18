# SQL데이터 베이스 및 파이썬 구동
import sqlite3

# 데이터 베이스 연결 / 데이터 입력&수정
connection = sqlite3.connect('certification.db')
cursor = connection.cursor()

# 테이블 생성 + 이미 있으면 생성안되니
cursor.execute('''
CREATE TABLE IF NOT EXISTS certification (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    birth TEXT NOT NULL,
    certificate_no TEXT NOT NULL,
    method TEXT NOT NULL,
    level TEXT NOT NULL,
    issue_date TEXT NOT NULL,
    expiry_date TEXT NOT NULL
)
''')

# 변경사항 저장/ 종료
connection.commit()
connection.close()