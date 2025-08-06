import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'sim_DB')

def db_critical_populate():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS CriticalProps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chemical TEXT NOT NULL,
            Tc FLOAT,
            Pc FLOAT
            )
            ''')

def add_critical_entry(chemical, Tc, Pc):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
        INSERT OR IGNORE INTO CriticalProps (chemical, Tc, Pc)
        VALUES (?, ?, ?)
        ''', (chemical, Tc, Pc))

        if cursor.rowcount>0:
            print(f"successfully added {chemical} to the table")
        else:
            print(f"{chemical} entry could not be added")

def add_many_critical_entry(list):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.executemany('''
        INSERT OR IGNORE INTO CriticalProps (chemical, Tc, Pc)
        VALUES (?, ?, ?)
        ''', list)

def get_all_critical_entries():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM CriticalProps')
        return cursor.fetchall()

def get_all_critical_entries_by_chem(chemical):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM CriticalProps WHERE chemical= ?', (chemical,))
        return cursor.fetchall()

def clearcrittable():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM CriticalProps")
    conn.commit()
    cursor.close()
    conn.close()

def readtable():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM CriticalProps')
        rows = cursor.fetchall()
        for row in rows:
            print(row)

def grabTcPc(name):
    entry = get_all_critical_entries_by_chem(name)
    Tc = entry[0][2]
    Pc = entry[0][3]
    return (Tc, Pc)

def main():
    db_critical_populate()

if __name__ == '__main__':
    readtable()
    # with sqlite3.connect(DB_PATH) as conn:
    #     cursor = conn.cursor()
    #     cursor.execute("DROP TABLE IF EXISTS CriticalProps")
    #     conn.commit()
    #     print("CriticalProps table has been deleted")
    #main()