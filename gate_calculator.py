# This program contains information about quantum gates
import numpy as np
import sympy as sp
import math
import random

class GateCalculator:
    #gate information
    I_GATE=sp.Matrix([[1,0],[0,1]])#  I-gate
    X_GATE=sp.Matrix([[0,1],[1,0]])#  X-gate
    Y_GATE=sp.Matrix([[0,-sp.I],[sp.I,0]])#  Y-gate
    Z_GATE=sp.Matrix([[1,0],[0,-1]]) #  Z-gate
    H_GATE=1/sp.sqrt(2) * sp.Matrix([[1,1],[1,-1]]) #  H-gate
    S_GATE=sp.Matrix([[1,0],[0,sp.I]]) #  S-gate
    S_DAGGER_GATE=lambda: sp.conjugate(GateCalculator.S_GATE) #  S dagger-gate
    T_GATE=sp.Matrix([[1,0],[0,1/sp.sqrt(2)*(1+sp.I)]]) #  T-gate     
    T_DAGGER_GATE=lambda: sp.conjugate(GateCalculator.T_GATE) #  T dagger-gate
    p_gate = lambda phi: sp.Matrix([1,0],[0,sp.exp**{sp.I * phi}]) #  P-gate
    # p_dagger_gate = lambda: sp.conjugate(GateCalculator.p_gate) #  P dagger-gate
    # rx_gate = lambda theta: sp.Matrix([sp.cos(sp.Rational(theta,2)),-sp.I*sp.sin(sp.Rational(theta,2))],[-sp.I*sp.sin(sp.Rational(theta,2)),sp.cos(sp.Rational(theta,2))]) #  Rx-gate
    # rx_dagger_gate = lambda: sp.conjugate(GateCalculator.rx_gate) #  Rx-dagger-gate
    # ry_gate = lambda theta: sp.Matrix([sp.cos(sp.Rational(theta,2)),-sp.sin(sp.Rational(theta,2))],[sp.sin(sp.Rational(theta,2)),sp.cos(sp.Rational(theta,2))]) #Ry-gate
    # rz_gate = lambda theta: sp.Matrix([sp.exp**(-sp.I*sp.Rational(theta,2)),0],[0,sp.exp**(sp.I*sp.Rational(theta,2))]) #  Rz-gate
    # rz_dagger_gate = lambda: sp.conjugate(GateCalculator.rz_gate) #  Rz-dagger-gate
    # u_gate = lambda theta, phi, Lambda: sp.Matrix([sp.cos(sp.Rational(theta,2)),-sp.exp**(sp.I*Lambda)*sp.sin(sp.Rational(theta,2))],[sp.exp**(sp.I*phi)*sp.sin(sp.Rational(theta,2)), sp.exp**(sp.I*(Lambda+phi))*sp.cos(sp.Rational(theta,2))]) #  U-gate
    # u_dagger_gate = lambda: sp.conjugate(GateCalculator.u_gate) #  U-dagger-gate

    #constructor
    def __init__(self):
        self.result_product = 0
        self.result_analysis = ""

    def calc(self,g,psi,p_phi):
        #initialize 1 column gate info (u) and f, and v matrix
        for j in range(len(g[0])):  #  loop by column of matrix g
            f = sp.Matrix([[1]])
            v = sp.Matrix([[1]])
            for i in range(len(g)):  #  loop by row of matrix g
                if g[i][j]=='c':
                    f = self.ten_product(f, sp.Matrix([[0,0],[0,1]]))
                    v = self.ten_product(v, GateCalculator.I_GATE)
                else:
                    f = self.ten_product(f, GateCalculator.I_GATE)
                    if g[i][j]=='x':
                        v=self.ten_product(v, GateCalculator.X_GATE)
                    elif g[i][j]=='y':
                        v=self.ten_product(v, GateCalculator.Y_GATE)
                    elif g[i][j]=='z':
                        v=self.ten_product(v, GateCalculator.Z_GATE)
                    elif g[i][j]=='h':
                        v=self.ten_product(v, GateCalculator.H_GATE)
                    elif g[i][j]=='s':
                        v=self.ten_product(v, GateCalculator.S_GATE)
                    elif g[i][j]=='t':
                        v=self.ten_product(v, GateCalculator.T_GATE)
                    elif g[i][j]=='i':
                        v=self.ten_product(v, GateCalculator.I_GATE)
                    elif g[i][j]=='sd':
                        v=self.ten_product(v, GateCalculator.S_DAGGER_GATE())
                    elif g[i][j]=='td':
                        v=self.ten_product(v, GateCalculator.T_DAGGER_GATE())
                    elif g[i][j]=='measure':
                        v=self.ten_product(v, GateCalculator.I_GATE)
                        psi=self.measure(len(g),i,psi)*psi
                    elif g[i][j]=='p':
                        v=self.ten_product(v, GateCalculator.p_gate(p_phi[i][j]))  
                    # elif g[i][j]=='pd':
                    #     v=self.ten_product(v, GateCalculator.p_dagger_gate())
                    # elif g[i][j]=='rx':
                    #     v=self.ten_product(v, GateCalculator.rx_gate())
                    # elif g[i][j]=='rxd':
                    #     v=self.ten_product(v, GateCalculator.rx_dagger_gate())
                    # elif g[i][j]=='ry':
                    #     v=self.ten_product(v, GateCalculator.ry_gate())
                    # elif g[i][j]=='rz':
                    #     v=self.ten_product(v, GateCalculator.rz_gate())
                    # elif g[i][j]=='rzd':
                    #     v=self.ten_product(v, GateCalculator.rz_dagger_gate())
                    # elif g[i][j]=='u':
                    #     v=self.ten_product(v, GateCalculator.u_gate())
                    # elif g[i][j]=='ud':
                    #     v=self.ten_product(v, GateCalculator.u_dagger_gate())
            u = f*v - f + sp.eye(2**len(g))
            psi = u*psi
        return self.standardize(psi)
    
    #calculate "vecA self vecB"
    def ten_product(self, a, b):
        result = sp.zeros(a.shape[0]*b.shape[0],a.shape[1]*b.shape[1])
        for i in range(a.shape[0]*b.shape[0]):
            for j in range(a.shape[1]*b.shape[1]):
                result[i,j] = a[math.floor(i/b.shape[0]),math.floor(j/b.shape[1])]*b[i%b.shape[0],j%b.shape[1]]
        return result

    #analysis vector as "sum of basis"
    def ten_analysis(self, vector):
        self.result_analysis = ""
        counter=0
        for i in range(len(vector)):
            if vector[i,0]!=0:
                if counter>0:
                    if sp.re(vector[i,0])>0 or (sp.re(vector[i,0]) == 0 and sp.im(vector[i,0])>0):
                        self.result_analysis += "+"
                if vector[i,0]==1:
                    self.result_analysis += self.vec_analysis(i,int(math.log2(len(vector))))
                else:
                    self.result_analysis+=str(vector[i,0])+self.vec_analysis(i,int(math.log2(len(vector))))
                counter+=1
        return self.result_analysis
    
    def vec_analysis(self, number,size):
        return "|"+bin(number)[2:].zfill(size)+">"

    def measure(self,n,i,psi):
        operator=sp.Matrix([[1]])
        if random.random() < 1/(1+(abs(psi[0])**2/abs(psi[2**(n-i-1)])**2)):
            for k in range(n):
                if k==i:
                    operator=self.ten_product(operator,sp.Matrix([[0,0],[0,1]]))
                else:
                    operator=self.ten_product(operator,GateCalculator.I_GATE)
        else:
            for k in range(n):
                if k==i:
                    operator=self.ten_product(operator,sp.Matrix([[1,0],[0,0]]))
                else:
                    operator=self.ten_product(operator,GateCalculator.I_GATE)
        return operator

    def standardize(self,psi):
        A = 0
        for i in  range(len(psi)):
            A += sp.Abs(psi[i])**2
        A = sp.sqrt(1/A)
        return A*psi