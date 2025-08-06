import numpy as np

def calculate_fugacity_coeff(z,T,P,x1,x2,a11,a22,a12,b1,b2,component):
    R = 0.08314
    b_mix = x1*b1 + x2*b2
    a_mix = x1**2 * a11 + 2*x1*x2*a12 + x2**2 * a22

    A_mix = a_mix * P / (R**2 * T**2)
    B_mix = b_mix* P / (R*T)

    if component ==1 :
        bi = b1
        delta_ai = 2*(x1*a11+x2*a12)
    else:
        bi = b2
        delta_ai = 2*(x1*a12+x2*a22)

    ln_phi = (bi/b_mix) * (z - 1) - np.log(z - B_mix) - (A_mix/(2*np.sqrt(2)*B_mix)) * (delta_ai/a_mix - bi/b_mix) * np.log((z + (1+np.sqrt(2))*B_mix)/(z - (1-np.sqrt(2))*B_mix))
    return np.exp(ln_phi)