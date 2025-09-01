import sqlite3

conn = sqlite3.connect('larm.db')
cursor = conn.cursor()


cursor.execute('''CREATE TABLE IF NOT EXISTS sensor (
                    id INTEGER PRIMARY KEY,
                    navn TEXT,
                    lokale TEXT,
                    lokation TEXT
                )''')


cursor.execute('''CREATE TABLE IF NOT EXISTS data (
                    tid INTEGER,
                    db INTEGER,
                    lokale TEXT,
                    lokation TEXT,
                    sensor_id INTEGER,
                    FOREIGN KEY (sensor_id) REFERENCES sensor(id)
                )''')


cursor.execute("SELECT COUNT(*) FROM sensor")
amount = cursor.fetchone()[0]
if amount == 0:
    print("insert sensor")
    cursor.execute("INSERT INTO sensor (id, navn, lokale, lokation) VALUES (67, 'Zakarias', '2349', 'vindue')")

cursor.execute("SELECT COUNT(*) FROM data")
amount = cursor.fetchone()[0]

if amount == 0:
    print("insert data")
    cursor.execute("INSERT INTO data (tid, lokale, lokation, db, sensor_id) VALUES (unixepoch(), '2349', 'vindue', 90, 67)")
    cursor.execute("INSERT INTO data (tid, lokale, lokation, db, sensor_id) VALUES (unixepoch()+10, '2349', 'vindue', 80, 67)")
    cursor.execute("INSERT INTO data (tid, lokale, lokation, db, sensor_id) VALUES (unixepoch()+20, '2349', 'vindue', 65, 67)")

conn.commit()



cursor.close()
conn.close()
