from flask import Flask, render_template, request
import sqlite3
from collections import defaultdict

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    id_input = request.args.get('id', '').strip()
    name_input = request.args.get('name', '').strip()
    birth_input = request.args.get('birth', '').strip()

    if not id_input and not name_input and not birth_input:
        return render_template('ktc_korea.html')

    try:
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
                    SELECT name, birth, certificate_no, method, level, issue_date, expiry_date, sector
                    FROM certification
                    WHERE {' OR '.join(conditions)}
                '''
                cursor.execute(query, values)
                rows = cursor.fetchall()
            else:
                rows = []

        grouped_data = defaultdict(list)
        for row in rows:
            name, birth, certificate_no, method, level, issue_date, expiry_date, sector = row
            grouped_data[(name, birth)].append({
                'certificate_no': certificate_no,
                'method': method,
                'level': level,
                'issue_date': issue_date,
                'expiry_date': expiry_date,
                'sector' : sector
            })

        message = "No Data Found." if not grouped_data else ""
        return render_template('output_now.html', message=message, grouped_data=grouped_data)

    except sqlite3.Error as e:
        return render_template('output_now.html', message=f"데이터베이스 오류: {e}", grouped_data={})

# ✅ 이 부분이 있어야 Flask가 실행됨!
if __name__ == '__main__':
    app.run(debug=True)
