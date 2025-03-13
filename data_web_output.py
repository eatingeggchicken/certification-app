from flask import Flask, render_template, request
import sqlite3
from collections import defaultdict

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':  # 유저가 검색시
        id_input = request.form.get('id')
        name_input = request.form.get('name')
        birth_input = request.form.get('birth')

        # 데이터베이스 연결
        conn = sqlite3.connect('certification.db')
        cursor = conn.cursor()

        # 데이터 가져오기
        cursor.execute('''
            SELECT name, birth, certificate_no, method, level, issue_date, expiry_date
            FROM certification
            WHERE name = ? AND birth = ? AND certificate_no LIKE ?
        ''', (name_input, birth_input, f'%{id_input}%'))
        rows = cursor.fetchall()
        conn.close()
        
        # 추가 항목
        if not rows:
            return render_template('output_now.html', message="No Data Found.", grouped_data={}) # 안쓰는데 걍 빈칸으로 냅두는게 아쉽긴

        # 데이터를 이름과 생년월일을 기준으로 그룹화
        grouped_data = defaultdict(list)
        for row in rows:
            name, birth, certificate_no, method, level, issue_date, expiry_date = row
            grouped_data[(name, birth)].append({
                'certificate_no': certificate_no,
                'method': method,
                'level': level,
                'issue_date': issue_date,
                'expiry_date': expiry_date
            })
        
        

        return render_template('output_now.html', grouped_data=grouped_data)

    return render_template('ktc_korea.html') #페이지 띄우기

if __name__ == '__main__':
    app.run(debug=True)