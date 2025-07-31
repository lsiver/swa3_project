import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

from .kcalc import kcalculation
from .psat_calc import psat_calculation
#from ...api import convert_numpy_to_python

def convert_numpy_to_python(obj):
    if hasattr(obj, 'item'):
        return obj.item()
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    else:
        return obj

class BinDist:
    def __init__(self, LK, HK,xF1 = 0.5,xD_LK = 0.90, xB_LK = 0.05, q=1, R = 2.0,P=1.0):
        self.LK = LK
        self.HK = HK
        self.Nmin = 0
        self.stages = []
        self.stage_count = 0
        self.Nmin_stages = []
        self.Rmin = 0.0
        self.R = R
        self.q = q
        #Since I am not accounting for non-ideal behavior...pressure is sort of a waste of time here.
        # A future update
        self.P = P
        self.xF1 = xF1
        self.xF2 = 1 - xF1
        self.xD_LK = xD_LK
        self.xD_HK = 1 - xD_LK
        self.xB_LK = xB_LK
        self.xB_HK = 1 - xB_LK
        self.psatLK = 0
        self.psatHK = 0
        self.alpha_1_2 =1
        self.LK_HK_init()
        self.Rmin_calc()

    def LK_HK_init(self):
        #The order matters, could maybe solve all of this by switching the order in the API before it's even
        #sent to the backend. We'll see.
        psat1T = psat_calculation(self.LK)
        psat2T = psat_calculation(self.HK)
        if psat1T > psat2T:
            self.LK = self.LK
            self.HK = self.HK
            self.psatLK = psat1T
            self.psatHK = psat2T
            # self.xD_LK = self.xD_LK
            # self.xB_LK = self.xB_LK
            self.xF1 = self.xF1
        else:
            temp = self.LK
            self.LK = self.HK
            self.HK = temp
            self.psatLK = psat2T
            self.psatHK = psat1T
            # self.xD_LK = 1 - self.xD_LK
            # self.xB_LK = 1 - self.xB_LK
            self.xF1 = 1 - self.xF1
            # self.xD_HK = 1 - self.xD_LK
            # self.xB_HK = 1 - self.xB_LK
            self.xF2 = 1 - self.xF1

        self.alpha_1_2 = kcalculation(self.LK)/kcalculation(self.HK)

    def Nmin_calc(self):
        x = self.xD_LK

        x_vle = np.array([0.0, 0.05, 0.1, 0.15, 0.20, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65,
                          0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0])
        y_vle =self.alpha_1_2*x_vle/(1+x_vle*(self.alpha_1_2-1))
        vle = interp1d(x_vle, y_vle, kind='linear', fill_value="extrapolate")
        vle_inv = interp1d(y_vle,x_vle,kind='linear',fill_value="extrapolate")

        self.Nmin_stages = []
        current_y = vle(x)
        stage_count = 0

        while x > self.xB_LK and stage_count < 300:
            self.Nmin_stages.append((x, current_y))
            stage_count += 1

            y_next = x
            x = vle_inv(y_next)
            current_y = vle(x)

            if x < self.xB_LK:
                self.Nmin_stages.append((x,current_y))
                stage_count+=1

        self.Nmin = stage_count
        return self.Nmin

    def Rmin_calc(self):
        self.Rmin = 1/(self.xF1*(self.alpha_1_2 - 1))
        return self.Rmin

    def binary_distillation_calc(self):
        x = self.xD_LK
        self.R = max(self.Rmin,self.R)

        #Mass Balance
        F = 1000
        D = F * (self.xF1 - self.xB_LK) / (self.xD_LK - self.xB_LK)
        B = F - D
        L_rect = self.R * D
        V_rect = (self.R + 1) * D
        L_strip = L_rect + self.q * F
        V_strip = V_rect - (1 - self.q) * F

        x_vle = np.array([0.0, 0.05, 0.1, 0.15, 0.20, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65,
                          0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0])
        y_vle =self.alpha_1_2*x_vle/(1+x_vle*(self.alpha_1_2-1))
        vle = interp1d(x_vle, y_vle, kind='linear', fill_value="extrapolate")
        vle_inv = interp1d(y_vle,x_vle,kind='linear',fill_value="extrapolate")

        self.stages = []
        current_y = vle(x)
        self.stage_count = 0
        section = 'rectification'

        while x > self.xB_LK and self.stage_count < 300:
            self.stages.append((x, current_y, section))
            self.stage_count += 1

            if section == "rectification" and x > self.xF1:
                y_next = (L_rect / V_rect) * x + self.xD_LK / (self.R + 1)
            else:
                if section == "rectification":
                    section = "stripping"
                    feed_stage = self.stage_count
                y_next = (L_strip / V_strip) * x - (L_strip / V_strip - 1) * self.xB_LK

            x = vle_inv(y_next)
            current_y = vle(x)

        if x <= self.xB_LK:
            #self.stages.append((self.xB_LK, vle(self.xB_LK), "stripping"))
            self.stages.append((x,vle(x),"stripping"))
            self.stage_count += 1

    def get_plotting_data(self):
        # calculate the operating line
        R = self.R
        xF = self.xF1
        xD = self.xD_LK
        xB = self.xB_LK
        q = self.q

        # mass balance
        F = 1000
        D = F * (xF - xB) / (xD - xB)
        L_rect = R * D
        V_rect = (R + 1) * D
        L_strip = L_rect + q * F
        V_strip = V_rect - (1 - q) * F

        # VLE curve data
        x_vle = np.array([0.0, 0.05, 0.1, 0.15, 0.20, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65,
                          0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0])
        y_vle = self.alpha_1_2 * x_vle / (1 + x_vle * (self.alpha_1_2 - 1))
        # operating lines
        x_rect = np.linspace(self.xF1, self.xD_LK, 100)
        y_rect = (L_rect / V_rect) * x_rect + self.xD_LK / (self.R + 1)

        x_strip = np.linspace(self.xB_LK, self.xF1, 100)
        y_strip = (L_strip / V_strip) * x_strip - (L_strip / V_strip - 1) * self.xB_LK

        # fix the stages
        clean_stages = []
        for stage in self.stages:
            x, y, section = stage
            clean_stages.append([
                convert_numpy_to_python(x),
                convert_numpy_to_python(y),
                section
            ])

        # real mccabe-thiele steps
        steps = []
        for i in range(len(clean_stages) - 1):
            x_current, y_current, section_current = clean_stages[i]
            x_next, y_next, section_next = clean_stages[i + 1]

            # horizontal line to VLE curve
            steps.append({
                'x': [x_current, x_current],
                'y': [y_current, y_next],
                'type': 'horizontal'
            })

            # vertical line to operating line
            steps.append({
                'x': [x_current, x_next],
                'y': [y_next, y_next],
                'type': 'vertical'
            })

        plot_data = {
            'vle_curve': {
                'x': x_vle.tolist(),
                'y': y_vle.tolist()
            },
            'rectifying_line': {
                'x': x_rect.tolist(),
                'y': y_rect.tolist()
            },
            'stripping_line': {
                'x': x_strip.tolist(),
                'y': y_strip.tolist()
            },
            'steps': steps,
            'feed_point': {
                'x': convert_numpy_to_python(xF),
                'y': convert_numpy_to_python(xF)
            }
        }
        return plot_data


# #     #binary_distillation_calc("Benzene","Toluene", 0.2,0.99,0.01,1,2.0,True)
# tower = BinDist("Benzene","Toluene", 0.8,0.9,0.05,1)
# # #tower.binary_distillation_calc("Benzene","Toluene", 0.2,0.99,0.01,1,2.0,False)
# tower.LK_HK_init()
# print(tower.LK,tower.HK,tower.xF1,tower.xD_LK,tower.xD_HK, tower.xB_LK,tower.xB_HK,tower.psatLK,tower.psatHK)
# tower2 = BinDist("Toluene","Benzene", 0.8,0.95,0.05,1)
# tower2.LK_HK_init()
# print(tower2.LK,tower2.HK,tower2.xF1,tower2.xD_LK,tower2.xD_HK,tower2.xB_LK,tower2.xB_HK,tower2.psatLK,tower2.psatHK)
# tower2.Nmin_calc()
# print(tower2.Nmin)
# print(tower2.Nmin_stages)
# tower2.binary_distillation_calc()
# print(tower2.stages,tower2.stage_count)

