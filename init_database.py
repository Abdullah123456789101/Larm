import sqlite3

conn = sqlite3.connect('larm.db')
cursor = conn.cursor()


cursor.execute('''CREATE TABLE IF NOT EXISTS sensor (
                    id INTEGER PRIMARY KEY,
                    navn TEXT,
                    lokation TEXT,
                    lokale TEXT
                )''')


cursor.execute('''CREATE TABLE IF NOT EXISTS data (
                    tid INTEGER,
                    db INTEGER,
                    sensor_id INTEGER,
                    FOREIGN KEY (sensor_id) REFERENCES sensor(id)
                )''')


cursor.execute("SELECT COUNT(*) FROM sensor")
amount = cursor.fetchone()[0]
if amount == 0:
    print("insert sensor")
    cursor.execute("INSERT INTO sensor (id, navn, lokation, lokale) VALUES (67, 'Zakarias', 'vindue', '2349')")

cursor.execute("SELECT COUNT(*) FROM data")
amount = cursor.fetchone()[0]

if amount == 0:
    print("insert data")
    cursor.execute("INSERT INTO data (tid, db, sensor_id) VALUES (unixepoch(), 90, 67)")
    cursor.execute("INSERT INTO data (tid, db, sensor_id) VALUES (unixepoch()+10, 80, 67)")
    cursor.execute("INSERT INTO data (tid, db, sensor_id) VALUES (unixepoch()+20, 65, 67)")

conn.commit()

cursor.close()
conn.close()
