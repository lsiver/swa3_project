from unittest import TestCase

from chem.DA.kcalc import kcalculation

class TestKcalc(TestCase):
    def test_kcalc(self) -> None:
        k_toluene = kcalculation("Toluene",2)
        k_benzene = kcalculation("Benzene",2)
        assert(2.2 <= k_benzene/k_toluene <= 2.6)
