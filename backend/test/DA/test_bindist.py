from unittest import TestCase

from chem.DA.bindist import BinDist

class TestBinDist(TestCase):
    def test_BinDist(self) -> None:
        tower = BinDist("Toluene","Benzene",0.80,0.95,0.0050,1,4.0,1.0)
        tower.Nmin_calc()
        tower.Rmin_calc()
        tower.binary_distillation_calc()
        assert((tower.Nmin==11) and (3 <= tower.Rmin <= 4))