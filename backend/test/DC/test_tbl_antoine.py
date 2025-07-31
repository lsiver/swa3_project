from unittest import TestCase
import sqlite3
import os
from pathlib import Path

test_dir = Path(__file__).parent
DB_PATH = test_dir / '..' / '..' / 'chem' / 'DC' / 'sim_DB'
DB_PATH = DB_PATH.resolve()

from chem.DC.tbl_antoine import add_antoine_entry, cleartable

class TestAntoineTbl(TestCase):
    def test_add_antoine_entry(self) -> None:
        add_antoine_entry("TestCase",1,2,3,300,400)
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Antoine WHERE chemical= ?', ("TestCase",))
            test_values = cursor.fetchall()
        test_sum = test_values[0][2]+test_values[0][3]+test_values[0][4]+test_values[0][5]+test_values[0][6]
        cleartable()
        assert(test_sum == 706.0)

