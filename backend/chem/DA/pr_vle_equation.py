from .calculate_fugacity_coeff import calculate_fugacity_coeff
from .calculate_z_factor import calculate_z_factor


def vle_equations(x1, x2,y1,y2, T, P, a1, a2, a12, b1, b2):
    try:
        # liquid mixture params
        a_mix_L = x1**2 * a1 + 2*x1*x2*a12 + x2**2 * a2
        b_mix_L = x1 * b1 + x2 * b2
        z_L, _ = calculate_z_factor(T, P, a_mix_L, b_mix_L)

        #vapor mixture params
        a_mix_V = y1**2 * a1 + 2*y1*y2*a12 + y2**2 * a2
        b_mix_V = y1 * b1 + y2 * b2
        _, z_V = calculate_z_factor(T, P, a_mix_V, b_mix_V)

        phi_L1 = calculate_fugacity_coeff(z_L, T, P, x1, x2, a1, a2, a12, b1, b2, 1)
        phi_L2 = calculate_fugacity_coeff(z_L, T, P, x1, x2, a1, a2, a12, b1, b2, 2)
        phi_V1 = calculate_fugacity_coeff(z_V, T, P, y1, y2, a1, a2, a12, b1, b2, 1)
        phi_V2 = calculate_fugacity_coeff(z_V, T, P, y1, y2, a1, a2, a12, b1, b2, 2)

        K1 = phi_L1/phi_V1
        K2 = phi_L2/phi_V2

        y1_new = K1*x1
        y2_new = K2*x2

        return y1_new, y2_new

    except:
        return x1,x2