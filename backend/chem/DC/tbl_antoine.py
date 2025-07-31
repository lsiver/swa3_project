import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'sim_DB')

def db_antoine_populate():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Antoine (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chemical TEXT NOT NULL,
            A FLOAT,
            B FLOAT,
            C FLOAT,
            T1 FLOAT,
            T2 FLOAT
            )
            ''')

def add_antoine_entry(chemical, A, B, C, T1, T2):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
        INSERT OR IGNORE INTO Antoine (chemical, A, B, C, T1, T2)
        VALUES (?, ?, ?, ?, ? ,?)
        ''', (chemical, A, B, C, T1, T2))

        if cursor.rowcount>0:
            print(f"successfully added {chemical} to the table")
        else:
            print(f"{chemical} entry could not be added")

def add_many_antoine_entry(list):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.executemany('''
        INSERT OR IGNORE INTO Antoine (chemical, A, B, C, T1, T2)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', list)

def get_all_antoine_entries():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Antoine')
        return cursor.fetchall()

def get_all_antoine_entries_by_chem(chemical):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Antoine WHERE chemical= ?', (chemical,))
        return cursor.fetchall()

def cleartable():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Antoine")
    conn.commit()
    cursor.close()
    conn.close()

def readtable():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Antoine')
        rows = cursor.fetchall()
        for row in rows:
            print(row)

def main():
    db_antoine_populate()

if __name__ == '__main__':
    readtable()
    main()

