import sqlite3
from flask import Flask, render_template

app = Flask(__name__)

def get_certifications():
    # SQLite 데이터베이스 연결
    conn = sqlite3.connect("certification.db")
    cursor = conn.cursor()

    # 데이터 조회 (name과 birth를 기준으로 정렬)
    cursor.execute('''
        SELECT name, birth, certificate_no, method, level, issue_date, expiry_date 
        FROM certification
        ORDER BY name, birth
    ''')
    rows = cursor.fetchall()
    
    # 데이터베이스 연결 종료
    conn.close()

    # 데이터를 이름과 생년월일 기준으로 그룹화
    grouped_data = {}
    for row in rows:
        name, birth, certificate_no, method, level, issue_date, expiry_date = row
        key = (name, birth)  # 이름과 생년월일을 기준으로 그룹화
        if key not in grouped_data:
            grouped_data[key] = []
        grouped_data[key].append({
            "certificate_no": certificate_no,
            "method": method,
            "level": level,
            "issue_date": issue_date,
            "expiry_date": expiry_date
        })

    return grouped_data

@app.route('/')
def certificate_list():
    grouped_data = get_certifications()  # DB에서 데이터 가져오기
    return render_template("output_now.html", grouped_data=grouped_data)

if __name__ == '__main__':
    app.run(debug=True)