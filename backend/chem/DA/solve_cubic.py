import numpy as np

def solve_cubic(a,b,c,d):
    coeffs = [a,b,c,d]
    roots = np.roots(coeffs)

    real_roots = []
    for root in roots:
        if abs(root.imag) < 1e-10:
            real_roots.append(root.real)

    return sorted(real_roots)