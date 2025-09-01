from flask import Flask, jsonify, request
import sqlite3



app = Flask(__name__)



@app.route('/data', methods=['GET'])
def get_data():
    conn = sqlite3.connect('larm.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM data")
    data = cursor.fetchall()

    items = []
    for datapoint in data:
        items.append({
            "tid": datapoint[0],
            "db": datapoint[1],
            "lokale": datapoint[2],
            "lokation": datapoint[3],
            "sensor_id": datapoint[4]
        })

    cursor.close()
    conn.close()

    return jsonify(items)

@app.route('/data/<int:start>-<int:end>', methods=['GET'])
def get_data_date(start, end):
    conn = sqlite3.connect('larm.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM data WHERE tid >= ? AND tid <= ?", (start, end))
    data = cursor.fetchall()

    items = []
    for datapoint in data:
        items.append({
            "tid": datapoint[0],
            "db": datapoint[1],
            "lokale": datapoint[2],
            "lokation": datapoint[3],
            "sensor_id": datapoint[4]
        })

    cursor.close()
    conn.close()

    return jsonify(items)


# get sensor data
@app.route('/sensor/<int:sensor_id>/<int:start>-<int:end>', methods=['GET'])
def get_sensor_data(sensor_id, start, end):
    return jsonify([sensor_id, start, end])





if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
