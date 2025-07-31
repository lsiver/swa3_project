from .psat_calc import psat_calculation


def kcalculation(chemical,P=1.0,T=100.0):
    return psat_calculation(chemical)/P