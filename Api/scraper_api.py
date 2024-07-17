from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)

DB_USER = #db username here
DB_PASSWORD = #db password here
DB_HOST = #db host here
DB_DATABASE = #db name here
DB_PORT = #db port here default usually is 5432

@app.route('/data')
def get_data():
    data = []
    try:
        con = psycopg2.connect(user=DB_USER, password=DB_PASSWORD,
                            host=DB_HOST, database=DB_DATABASE, port=DB_PORT)
        cur = con.cursor()
        cur.execute("SELECT * FROM standford_financial;")
        con.commit()
        data = cur.fetchall()
        cur.close()
        con.close
    except Exception as e:
        return jsonify({"Error":str(e)}), 500
    return jsonify(data)
if __name__ == '__main__':
    app.run(debug=True)