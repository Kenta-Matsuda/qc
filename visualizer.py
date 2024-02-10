import sympy as sp
import math
import matplotlib
matplotlib.use("TkAgg")

class Visualizer:
    def __init__(self, psi):
        self.psi = psi
        self.p_array = sp.zeros(len(psi), 1)
        self.phi_array = sp.zeros(len(psi), 1)
        self.bit_number = int(math.log2(len(self.psi)))
        self.hamming_array = [[] for j in range(self.bit_number+1)]
        self.transform()
        self.hamming()
    
    def degree(self,a):
        if a==0:
            return 0
        else:
            return sp.arg(a)
    
    def transform(self):
        self.phi_array[0] = 0
        for i in range(len(self.psi)):
            self.p_array[i] = sp.Abs(self.psi[i])**2
            if self.degree(self.psi[i]*sp.E**(-sp.I*self.degree(self.psi[0]))) < 0:
                self.phi_array[i] = 2*sp.pi + self.degree(self.psi[i]*sp.E**(-sp.I*self.degree(self.psi[0])))
            else:
                self.phi_array[i] = self.degree(self.psi[i]*sp.E**(-sp.I*self.degree(self.psi[0])))

    def hamming(self):
        for i in range(len(self.psi)):
            number = i
            counter = 0
            while number>0:
                if number%2==1:
                    counter+=1
                number = number // 2
            self.hamming_array[counter].append(i)