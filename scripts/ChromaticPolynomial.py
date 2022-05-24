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
# nCk*(x)*(x-1)*....(x-k+1) / k!
class ChromaticPolynomial:
    def __init__(self):
        self.degree = 0
        self.prime = 97
    def combExpr(self, k):
        expr = 1
        x = symbols('x')
        for i in range(0, k):
            expr *= (x - i)
        return expr/math.factorial(k)

    def reduced_expr(self, polynomial):
        x = symbols('x')
        # print("Received polynomial = " + str(polynomial))
        # print("Degree = " + str(self.degree))
        res_expr = 0
        res_expr += polynomial.subs(x, 0)
        for i in range(1, self.degree + 1):
            coefficient = polynomial.coeff(x**i)
            # print(print("Current coefficient = " + str(coefficient)))
            coefficient = int(coefficient) % self.prime
            # print("Current coefficient after mod = " + str(coefficient))
            res_expr += coefficient * (x**i)
        return res_expr

    def getPolynomial(self,num):
        x = symbols('x')
        expr = 0
        matrix = PreProcess().getAdjacencyMatrix(num)
        vertices = len(matrix)
        self.degree = vertices
        chromaticNumber = DeterMineChromaticNumber().getChromaticNumber(matrix)
        for i in range (chromaticNumber, vertices+1):
            expr += (ChromaticCoefficient().getCoefficient(matrix, i))*(self.combExpr(i))
        print("Chromatic Polynomial in non expanded Form = \n" + str(expr) + "\n")
        expanded_expr = expand(expr)
        result = self.reduced_expr(expanded_expr)
        print("Chromatic polynomial in expanded form = \n" + str(result) + "\n")
        return result
    def getPolynomialWithString(self,binary):
        x = symbols('x')
        expr = 0
        matrix = PreProcess().getAdjacencyMatrixWithString(binary)
        vertices = len(matrix)
        self.degree = vertices
        chromaticNumber = DeterMineChromaticNumber().getChromaticNumber(matrix)
        for i in range(chromaticNumber, vertices + 1):
            expr += (ChromaticCoefficient().getCoefficient(matrix, i)) * (self.combExpr(i))
        # print("Chromatic Polynomial in non expanded Form = \n" + str(expr) + "\n")
        expanded_expr = expand(expr)
        result = self.reduced_expr(expanded_expr)
        print("Chromatic polynomial in expanded form = \n" + str(result) + "\n")
        return result

