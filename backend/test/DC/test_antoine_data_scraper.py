from unittest import TestCase

from chem.DC.antoine_data_scraper import get_all_antoine_coef
from chem.DC.tbl_antoine import add_antoine_entry, cleartable

class TestAntoineDataScraper(TestCase):
    def test_get_all_antoine_coef(self) -> None:
        T,A,B,C = get_all_antoine_coef("Benzene")
        psat = 10**(A[0] - B[0]/(C[0]+373))
        assert(1.7 <= psat <= 1.9)
