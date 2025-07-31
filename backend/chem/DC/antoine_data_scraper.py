from requests import get
from bs4 import BeautifulSoup
from contextlib import closing
import csv
from .tbl_antoine import add_antoine_entry, cleartable, add_many_antoine_entry

'''
Some of this is sourced from https://github.com/MUCTR3/NISTAntoine/blob/master/antoine.py
'''

def get_all_antoine_coef(Name):
    table = get_html_table(Name)

    rows = table.find_all('tr', class_='exp')

    Temperatures, As, Bs, Cs = [], [], [], []

    for row in rows:
        cols = row.find_all('td')

        As.append(float(cols[1].text))
        Bs.append(float(cols[2].text))
        Cs.append(float(cols[3].text))

        parts = cols[0].text.split(" to ")
        lower_lim = float(parts[0])
        higher_lim = float(parts[1])
        Temperatures.append([lower_lim, higher_lim])

    return Temperatures, As, Bs, Cs

def get_html_table(Name):
    # https://webbook.nist.gov/cgi/cbook.cgi?Name=methane&Mask=4.
    url = str.format('https://webbook.nist.gov/cgi/cbook.cgi?Name={0}&Mask=4', Name.lower())

    raw_html = get_response(url)

    html = BeautifulSoup(raw_html, 'html.parser')

    table = html.find('table', attrs={'aria-label': 'Antoine Equation Parameters'})

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

def populate_antoine_from_NIST(name):
    Temperatures, As, Bs, Cs = get_all_antoine_coef(name)
    for i in range(len(Temperatures)):
        add_antoine_entry(name,As[i],Bs[i],Cs[i],Temperatures[i][0],Temperatures[i][1])

def build_antoine_list():
    cleartable()
    chemical_list = ["Methane", "Ethane","Ethylene","Propane","Butane","Pentane","Hexane","Toluene","Benzene"]
    for chemical in chemical_list:
        populate_antoine_from_NIST(chemical)

def build_antoine_list_oneshot():
    cleartable()
    chemical_list = ["Methane", "Ethane","Ethylene","Propane","Butane","Pentane","Hexane","Toluene","Benzene"]
    big_list = []
    for chemical in chemical_list:
        Temperature, A, B, C = get_all_antoine_coef(chemical)
        temp_tuple = (chemical, A[0],B[0],C[0],Temperature[0][0],Temperature[0][1])
        big_list.append(temp_tuple)
    add_many_antoine_entry(big_list)

def main():
    build_antoine_list()

if __name__ == '__main__':
    main()