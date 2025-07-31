import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'sim_DB')

def create_database():
    conn = sqlite3.connect(DB_PATH)
    cursor=conn.cursor()
    conn.commit()
    conn.close()

def __main__():
    create_database()

if (__name__ == '__main__'):
    __main__()
#create_database()