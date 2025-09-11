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

@app.route('/sensor_info/<int:sensor_id>', methods=['GET'])
def get_sensor_info(sensor_id):
    return jsonify(query_db("SELECT * FROM sensor WHERE id = ?", (sensor_id, )))

@app.route('/sensor/<int:sensor_id>', methods=['GET'])
def get_sensor(sensor_id):
    return jsonify(query_db("SELECT * FROM data WHERE sensor_id = ?", (sensor_id, )))


@app.route('/sensor/<int:sensor_id>/<int:start>-<int:end>', methods=['GET'])
def get_sensor_date(sensor_id, start, end):
    return jsonify(query_db("SELECT * FROM data WHERE sensor_id = ? AND tid BETWEEN ? AND ?", (sensor_id, start, end)))

# teste uploading af data:
# Invoke-RestMethod -Uri "http://127.0.0.1:8080/add" -Method Post ` -ContentType "application/json" ` -Body '{ "db": 90, "sensor_id": 67 }'
@app.route('/add', methods=['POST'])
def add_data():
    data = request.get_json()
    db = data['db']
    sensor_id = data['sensor_id']

    conn = sqlite3.connect('larm.db')
    cursor = conn.cursor()

    cursor.execute("SELECT lokale, lokation FROM sensor WHERE id = ?", (sensor_id, ))
    lokale, lokation = cursor.fetchone()

    cursor.execute("INSERT INTO data (tid, db, lokale, lokation, sensor_id) VALUES (unixepoch(), ?, ?, ?, ?)",
                   (db, lokale, lokation, sensor_id))
    conn.commit()

    conn.close()

    return jsonify({'message': 'Data added successfully'})

# Invoke-RestMethod -Uri "http://127.0.0.1:8080/update_sensor" -Method Put ` -ContentType "application/json" ` -Body '{ "sensor_id": 67, "lokale": "2221", "lokation": "doer" }'
@app.route('/update_sensor', methods=['PUT'])
def update_sensor():
    data = request.get_json()

    sensor_id = data['sensor_id']
    lokale = data['lokale']
    lokation = data['lokation']

    conn = sqlite3.connect('larm.db')
    cursor = conn.cursor()

    cursor.execute('UPDATE sensor SET lokale = ?, lokation = ? WHERE id = ?', (lokale, lokation, sensor_id))
    conn.commit()

    conn.close()
    return jsonify({'message': 'Sensor updated successfully'})




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
