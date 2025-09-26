from flask import Flask, render_template, jsonify, request, redirect, url_for
import sqlite3

from datetime import datetime

from helpers import query_db, make_graf


app = Flask(__name__, template_folder="Templates")

@app.route('/', methods=['GET', 'POST'])
def root():
    if request.method == 'GET':
        return render_template("index.html")

    lokale = request.form.get("lokale")
    sensor = request.form.get("sensor")
    all_data = request.form.get("all")
    start = request.form.get("start")
    end = request.form.get("end")

    # Konverter dato fra yyyy-mm-dd til unix timestamp, hvis start og end er sat
    start_ts = int(datetime.strptime(start, "%Y-%m-%d").timestamp()) if start else None
    end_ts = int(datetime.strptime(end, "%Y-%m-%d").timestamp()) if end else None

    if sensor:
        if start_ts and end_ts:
            return redirect(url_for("get_sensor_date", sensor_id=sensor, start=start_ts, end=end_ts))
        else:
            return redirect(url_for("get_sensor", sensor_id=sensor))

    elif lokale:
        if start_ts and end_ts:
            return redirect(url_for("get_lokale_date", lokale=lokale, start=start_ts, end=end_ts))
        else:
            return redirect(url_for("get_lokale", lokale=lokale))

    elif all_data:
        if start_ts and end_ts:
            return redirect(url_for("get_data_date", start=start_ts, end=end_ts))
        else:
            return redirect(url_for("get_data"))

    # fallback
    return redirect(url_for("root"))


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

    tid = int(datetime.now().timestamp())

    cursor.execute("INSERT INTO data (tid, db, lokale, lokation, sensor_id) VALUES (?, ?, ?, ?, ?)",
                   (tid, db, lokale, lokation, sensor_id))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Data added successfully'})

# teste opdatere sensor
# Invoke-RestMethod -Uri "http://127.0.0.1:8080/update_sensor" -Method Put ` -ContentType "application/json" ` -Body '{ "sensor_id": 67, "lokale": "2221", "lokation": "vindue" }'
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
