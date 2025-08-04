from unittest import TestCase

from chem.DA.psat_calc import psat_calculation

class TestPsatCalc(TestCase):
    def test_psat_calc(self) -> None:
        psat_toluene = psat_calculation("Toluene")
        psat_benzene = psat_calculation("Benzene")
        assert((0.7 <= psat_toluene <= 0.8) and (1.7 <= psat_benzene <= 1.9))
