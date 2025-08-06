import numpy as np

def calculate_pr_parameters(T,Tc,Pc,omega):
    R = 0.08314
    Tr = T/ Tc

    kappa = 0.37464 + 1.54226 * omega - 0.26992 * omega**2
    alpha = (1 + kappa*(1 - np.sqrt(Tr)))**2

    a = 0.45724 * R**2 * Tc**2 * alpha/Pc
    b = 0.07780 * R * Tc/ Pc

    return a,b