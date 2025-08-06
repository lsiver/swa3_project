import math

from .psat_calc import psat_calculation

def acentric(name,Tc, Pc):
    prs = psat_calculation(name,0.7*Tc-273) / Pc
    w = -math.log10(prs) - 1
    return w
