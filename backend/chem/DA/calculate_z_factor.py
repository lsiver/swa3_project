from .solve_cubic import solve_cubic


def calculate_z_factor(T,P,a,b):
    #compressibility factor, Z
    R = 0.08314
    A = a*P / (R**2*T**2)
    B = b*P / (R*T)

    coeffs = [1,
              -(1-B),
              A - 3*B**2 - 2*B,
              -(A*B - B**2 - B**3)]

    roots = solve_cubic(*coeffs)

    if len(roots) == 1:
        z_liquid = z_vapor = roots[0]
    else:
        valid_roots = []
        for r in roots:
            if r > 0:
                valid_roots.append(r)
        if valid_roots:
            z_liquid = min(valid_roots)
            z_vapor = max(valid_roots)
        else:
            z_liquid = roots[0]
            z_vapor = roots[-1]

    return z_liquid, z_vapor