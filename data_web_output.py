from flask import Flask, render_template, request
import sqlite3
from collections import defaultdict

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':  # 유저가 검색할 때
        id_input = request.form.get('id', '').strip()
        name_input = request.form.get('name', '').strip()
        birth_input = request.form.get('birth', '').strip()

        # 입력값 검증
        if not id_input and not name_input and not birth_input:
            return render_template('output_now.html', message="Please enter at least one item.", grouped_data={})
        
        
        try:
            # 데이터베이스 연결 및 데이터 가져오기
            with sqlite3.connect('certification.db') as conn:
                cursor = conn.cursor()
                
                conditions = []
                values = []
                
                if name_input:
                    conditions.append("name = ?")
                    values.append(name_input)
                if birth_input:
                    conditions.append("birth = ?")
                    values.append(birth_input)
                if id_input:
                    conditions.append("certificate_no LIKE ?")
                    values.append(f"%{id_input}%") 

                if conditions:
                    query = f'''
                        SELECT name, birth, certificate_no, method, level, issue_date, expiry_date
                        FROM certification
                        WHERE {' OR '.join(conditions)}
                    '''
                    cursor.execute(query, values)
                    rows = cursor.fetchall()
                else:
                    rows = []
              

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

            # 메시지 추가
            message = "No Data Found." if not grouped_data else ""
            return render_template('output_now.html', message=message, grouped_data=grouped_data)

        except sqlite3.Error as e:
            return render_template('output_now.html', message=f"데이터베이스 오류: {e}", grouped_data={})

    return render_template('ktc_korea.html')  # 검색 페이지 렌더링

if __name__ == '__main__':
    app.run(debug=True)