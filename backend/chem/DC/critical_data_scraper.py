from requests import get
from bs4 import BeautifulSoup
from contextlib import closing
import csv

from .tbl_critical import add_critical_entry, clearcrittable, add_many_critical_entry, readtable

def get_critical_props(Name):
    table = get_html_table(Name)

    rows = table.find_all('tr',class_='cal')

    Tc, Pc = None, None

    for row in rows:
        cols = row.find_all('td')

        if len(cols) >= 2:
            first_col_text = cols[0].get_text(strip=True)

            if 'T' in first_col_text and cols[0].find('sub') and 'c' in cols[0].find('sub').text:
                value_text = cols[1].text.strip()
                Tc = float(value_text.split('±')[0])

            elif 'P' in first_col_text and cols[0].find('sub') and 'c' in cols[0].find('sub').text:
                value_text = cols[1].text.strip()
                Pc = float(value_text.split('±')[0])

    return Tc, Pc

def get_html_table(Name):
    # https://webbook.nist.gov/cgi/cbook.cgi?Name=methane&Mask=4.
    url = str.format('https://webbook.nist.gov/cgi/cbook.cgi?Name={0}&Mask=4', Name.lower())

    raw_html = get_response(url)

    html = BeautifulSoup(raw_html, 'html.parser')

    table = html.find('table', attrs={'aria-label': 'One dimensional data'})

    return table

def get_response(url):

    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except:
        print('Not found')
        return None

def is_good_response(resp):
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)

def populate_critical_from_NIST(name):
    Tc, Pc = get_critical_props(name)
    if name == "Water":
        Tc, Pc = (647.0, 220.0)
    add_critical_entry(name,Tc,Pc)

def build_critical_list():
    clearcrittable()
    chemical_list = ["Methane", "Ethane","Ethylene","Propane","Butane","Pentane","Hexane","Toluene","Benzene","Water", "Ethanol", "Acetone"]
    for chemical in chemical_list:
        populate_critical_from_NIST(chemical)

def build_critical_list_oneshot():
    clearcrittable()
    chemical_list = ["Methane", "Ethane","Ethylene","Propane","Butane","Pentane","Hexane","Toluene","Benzene","Water", "Ethanol", "Acetone"]
    big_list = []
    for chemical in chemical_list:
        Tc, Pc = get_critical_props(chemical)
        temp_tuple = (chemical, Tc, Pc)
        big_list.append(temp_tuple)
    add_many_critical_entry(big_list)

def main():
    build_critical_list()
    readtable()

if __name__ == '__main__':
    main()