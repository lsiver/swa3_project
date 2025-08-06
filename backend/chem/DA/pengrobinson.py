from typing import List, Tuple
import numpy as np
from scipy.optimize import fsolve, root_scalar

from .calculate_pr_parameters import calculate_pr_parameters
from .pr_vle_equation import vle_equations
import matplotlib.pyplot as plt


class PengRobinsonEOS:
    def __init__(self):
        self.Tc1 = 0
        self.Pc1 = 0
        self.omega1 = 0
        self.Tc2 = 0
        self.Pc2 = 0
        self.omega2 = 0
        self.kij = 0

    def calculate_vle_point(self,x1,T,P):
        if x1 <= 0:
            return 0.0
        if x1 >= 1:
            return 1.0

        x2 = 1 - x1

        a1, b1 = calculate_pr_parameters(T, self.Tc1, self.Pc1,self.omega1)
        a2, b2 = calculate_pr_parameters(T, self.Tc2, self.Pc2,self.omega2)
        a12 = np.sqrt(a1*a2)*(1 - self.kij)

        y1 = x1
        y2 = 1 - y1

        damping = 0.5
        for i in range(100):
            y1_new, y2_new = vle_equations(x1,x2,y1,y2,T,P,a1,a2,a12,b1,b2)
            sum = y1_new + y2_new
            y1_norm = y1_new/sum
            y2_norm = y2_new/sum
            y1_next = damping*y1_norm + (1-damping)*y1
            y2_next = damping*y2_norm + (1-damping)*y2

            if (abs(y1_next - y1) < 1e-8):
                return y1_next
            y1 = y1_next
            y2 = y2_next

        return y1



    def generate_xy_data(self,T,P,num_points= 21):
        x1_values = np.linspace(0,1,num_points)
        y1_values = np.zeros_like(x1_values)

        for i,x1 in enumerate(x1_values):
            y1_values[i] = self.calculate_vle_point(x1, T, P)

        return x1_values, y1_values

def main():
    #Benzene
    PREOS = PengRobinsonEOS()
    PREOS.Tc1 = 513.9
    PREOS.Pc1 = 61.4
    PREOS.omega1 = 0.649
    PREOS.Tc2 = 647.1
    PREOS.Pc2 = 220.6
    PREOS.omega2 = 0.345
    PREOS.kij = -0.0364
    x1, y1 = PREOS.generate_xy_data(353,1,100)
    plt.figure(figsize=(10,8))
    plt.plot(x1,y1,'b-')
    plt.show()


    #print(PREOS.Tc1)

if __name__ == '__main__':
    main()