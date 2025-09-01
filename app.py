from flask import Flask, jsonify, request
import sqlite3



app = Flask(__name__)

def query_db(query, args=()):
    conn = sqlite3.connect('larm.db')
    conn.row_factory = sqlite3.Row  # rows behave like dicts
    cursor = conn.cursor()

    cursor.execute(query, args)
    rows = cursor.fetchall()

    conn.close()
    return [dict(row) for row in rows]


@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(query_db("SELECT * FROM data"))

@app.route('/data/<int:start>-<int:end>', methods=['GET'])
def get_data_date(start, end):
    return jsonify(query_db("SELECT * FROM data WHERE tid BETWEEN ? AND ?", (start, end)))

@app.route('/lokale/<lokale>', methods=['GET'])
def get_lokale(lokale):
    return jsonify(query_db("SELECT * FROM data WHERE lokale = ?", (lokale,)))

@app.route('/lokale/<lokale>/<int:start>-<int:end>', methods=['GET'])
def get_lokale_date(lokale, start, end):
    return jsonify(query_db("SELECT * FROM data WHERE lokale = ? AND tid BETWEEN ? AND ?", (lokale, start, end)))


# get sensor data
@app.route('/sensor/<int:sensor_id>/<int:start>-<int:end>', methods=['GET'])
def get_sensor(sensor_id, start, end):
    return jsonify([sensor_id, start, end])



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
