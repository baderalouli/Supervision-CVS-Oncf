import sqlite3
from pathlib import Path


DATABASE_PATH = Path("data/cvs_monitoring.db")


class Database:

    def __init__(self, database_path=DATABASE_PATH):

        self.database_path = database_path

        self.create_tables()

    def connect(self):

        return sqlite3.connect(
            self.database_path
        )

    def create_tables(self):

        connection = self.connect()

        cursor = connection.cursor()

        # Table des mesures
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS measurements (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                timestamp TEXT,

                voltage REAL,

                output_voltage REAL,

                current REAL,

                power REAL,

                temperature REAL,

                internal_temperature REAL,

                vibration REAL,

                fan INTEGER,

                battery REAL,

                efficiency REAL,

                protection_active INTEGER,

                status TEXT

            )
        """)

        # Table des alarmes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alarms (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                timestamp TEXT,

                code TEXT,

                type TEXT,

                severity TEXT,

                message TEXT,

                value REAL

            )
        """)

        connection.commit()

        connection.close()

    def insert_measurement(self, data, status):

        connection = self.connect()

        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO measurements (

                timestamp,
                voltage,
                output_voltage,
                current,
                power,
                temperature,
                internal_temperature,
                vibration,
                fan,
                battery,
                efficiency,
                protection_active,
                status

            )

            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (

            data["timestamp"],

            data["voltage"],

            data["output_voltage"],

            data["current"],

            data["power"],

            data["temperature"],

            data["internal_temperature"],

            int(data["fan"]),

            data["vibration"],

            data["battery"],

            data["efficiency"],

            int(
                data.get(
                    "protection_active",
                    False
                )
            ),

            status

        ))

        connection.commit()

        connection.close()

    def insert_alarm(self, alarm, timestamp):

        connection = self.connect()

        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO alarms (

                timestamp,
                code,
                type,
                severity,
                message,
                value

            )

            VALUES (?, ?, ?, ?, ?, ?)
        """, (

            timestamp,

            alarm["code"],

            alarm["type"],

            alarm["severity"],

            alarm["message"],

            alarm["value"]

        ))

        connection.commit()

        connection.close()

    def get_measurements(self, limit=20):

        connection = self.connect()

        cursor = connection.cursor()

        cursor.execute("""
            SELECT *
            FROM measurements
            ORDER BY id DESC
            LIMIT ?
        """, (limit,))

        results = cursor.fetchall()

        connection.close()

        return results

    def get_alarms(self, limit=20):

        connection = self.connect()

        cursor = connection.cursor()

        cursor.execute("""
            SELECT *
            FROM alarms
            ORDER BY id DESC
            LIMIT ?
        """, (limit,))

        results = cursor.fetchall()

        connection.close()

        return results