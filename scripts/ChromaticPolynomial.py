import math

from sympy import *

from scripts.PreProcess import *
from scripts.DeterMineChromaticNumber import *
from scripts.ChromaticCoefficient import *
# features in need
# x = symbols('x')
# expr = x*(x-1)*(x-2) + x*(x-1)*(x-2)*(x-3)
# expanded_expr = expand(expr)
# print(expr)
# print(expand(expr))
# print(expr.subs(x, 5))
# print(expanded_expr.coeff(x**3))

class ChromaticPolynomial:
    def combExpr(self, k):
        expr = 1
        x = symbols('x')
        for i in range(0, k):
            expr *= (x - i)
        return expr/math.factorial(k)
    def getPolynomial(self,num):
        x = symbols('x')
        expr = 0
        matrix = PreProcess().getAdjacencyMatrix(num)
        vertices = len(matrix)
        chromaticNumber = DeterMineChromaticNumber().getChromaticNumber(matrix)
        for i in range (chromaticNumber, vertices+1):
            expr += (ChromaticCoefficient().getCoefficient(matrix, i))*(self.combExpr(i))
        print("Chromatic Polynomial in non expanded Form = \n" + str(expr) + "\n")
        expanded_expr = expand(expr)
        print("Chromatic polynomial in expanded form = \n" + str(expanded_expr) + "\n")
        return expanded_expr
