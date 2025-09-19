from flask import Flask, render_template, jsonify, request, redirect, url_for
import sqlite3

from helpers import *


app = Flask(__name__)

@app.route('/', methods=['GET'])
def root():
    return render_template("inex.html")

@app.route("/submit", methods = ["GET"])
def scoobydoo():
    lokale = request.args.get("lokale")
    sensor = request.args.get("sensor")

    if sensor:  # hvis bruger skrev sensor-id
        return redirect(url_for("get_sensor", sensor_id=sensor))

    elif lokale:  # hvis bruger skrev lokale
        return redirect(url_for("get_lokale", lokale=lokale))
@app.route('/data', methods=['GET'])
def get_data():
    query = query_db("SELECT * FROM data")
    graf_html = make_graf(query, "tid", "db", "lokale")
    return render_template("graf.html", graf=graf_html)

@app.route('/data/<int:start>-<int:end>', methods=['GET'])
def get_data_date(start, end):
    query = query_db("SELECT * FROM data WHERE tid BETWEEN ? AND ?", (start, end))
    graf_html = make_graf(query, "tid", "db", "lokale")
    return render_template("graf.html", graf=graf_html)

@app.route('/lokale/<lokale>', methods=['GET'])
def get_lokale(lokale):
    query = query_db("SELECT * FROM data WHERE lokale = ?", (lokale,))
    graf_html = make_graf(query, "tid", "db", "sensor_id")
    return render_template("graf.html", graf=graf_html)

@app.route('/lokale/<lokale>/<int:start>-<int:end>', methods=['GET'])
def get_lokale_date(lokale, start, end):
    query = query_db("SELECT * FROM data WHERE lokale = ? AND tid BETWEEN ? AND ?", (lokale, start, end))
    graf_html = make_graf(query, "tid", "db", "sensor_id")
    return render_template("graf.html", graf=graf_html)

@app.route('/sensor/<int:sensor_id>', methods=['GET'])
def get_sensor(sensor_id):
    query = query_db("SELECT * FROM data WHERE sensor_id = ?", (sensor_id, ))
    graf_html = make_graf(query, "tid", "db", "lokale")
    return render_template("graf.html", graf=graf_html)

@app.route('/sensor/<int:sensor_id>/<int:start>-<int:end>', methods=['GET'])
def get_sensor_date(sensor_id, start, end):
    query = query_db("SELECT * FROM data WHERE sensor_id = ? AND tid BETWEEN ? AND ?", (sensor_id, start, end))
    graf_html = make_graf(query, "tid", "db", "lokale")
    return render_template("graf.html", graf=graf_html)

@app.route('/sensor_info/<int:sensor_id>', methods=['GET'])
def get_sensor_info(sensor_id):
    return jsonify(query_db("SELECT * FROM sensor WHERE id = ?", (sensor_id, )))

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

# teste opdatere sensor
# Invoke-RestMethod -Uri "http://127.0.0.1:8080/update_sensor" -Method Put ` -ContentType "application/json" ` -Body '{ "sensor_id": 67, "lokale": "2221", "lokation": "doer" }'
@app.route('/update_sensor', methods=['PUT'])
def update_sensor():
    data = request.get_json()

    sensor_id = data['sensor_id']
    lokale = data['lokale']
    lokation = data['lokation']

    if not (sensor_id or lokale or lokation):
        return jsonify({'message': 'sensor_id, lokale or lokation is null'}), 400

    conn = sqlite3.connect('larm.db')
    cursor = conn.cursor()

    cursor.execute('UPDATE sensor SET lokale = ?, lokation = ? WHERE id = ?', (lokale, lokation, sensor_id))
    conn.commit()

    conn.close()
    return jsonify({'message': 'Sensor updated successfully'})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
