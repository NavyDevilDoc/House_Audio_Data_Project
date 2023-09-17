import sqlite3

class DatabaseManager:
    def __init__(self, db_name):
        self.db_name = db_name
        self.create_audio_db_and_table()

    def create_audio_db_and_table(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS Audio_Data_Capture (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     timestamp TEXT,
                     counter INTEGER,
                     adc_value REAL,
                     db_value REAL)''')
        conn.commit()
        conn.close()

    def sample_audio_data(self, sample_size=50):
        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            c.execute(f"SELECT * FROM Audio_Data_Capture ORDER BY timestamp DESC LIMIT {sample_size}")
            rows = c.fetchall()
        return list(reversed(rows))

    def insert_audio_data_batch(self, data_list):
        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            c.executemany("""
            INSERT INTO Audio_Data_Capture (timestamp, counter, adc_value, db_value)
            VALUES (?, ?, ?, ?);
            """, data_list)
            conn.commit()
