import sys
import os
project_root = os.path.join(os.path.dirname(__file__), '..','..')
sys.path.append(os.path.abspath(project_root))
import config

from tbl_antoine import get_all_antoine_entries_by_chem

def psat_calculation(chemical,T=100.0):
    #Kelvin
    T +=273
    constants = get_all_antoine_entries_by_chem(chemical)
    for entries in constants:
        if entries[1] == chemical:
            #base constants
            A = entries[2]
            B = entries[3]
            C = entries[4]
            if (T > entries[5]) and (T < entries[6]):
                A = entries[2]
                B = entries[3]
                C = entries[4]
                break
    #units of Bar
    return 10**(A - (B/(T+C)))
