import sqlite3

conn = sqlite3.connect('larm.db')
cursor = conn.cursor()


cursor.execute('''CREATE TABLE IF NOT EXISTS sensor (
                    id INTEGER PRIMARY KEY,
                    navn TEXT,
                    lokation TEXT,
                    lokale TEXT
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS lokale (
                    id INTEGER PRIMARY KEY,
                    sensor_id INTEGER,
                    FOREIGN KEY (sensor_id) REFERENCES sensor(id)
                )''')


cursor.execute('''CREATE TABLE IF NOT EXISTS data (
                    tid INTEGER,
                    db INTEGER,
                    sensor_id INTEGER,
                    FOREIGN KEY (sensor_id) REFERENCES sensor(id)
                )''')

