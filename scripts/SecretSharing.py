from scripts.ChromaticPolynomial import *
from sympy import *


class SecretSharing:
    def __init__(self):
        self.power = 0
        self.chromatic_polynomial = 0
        self.extra_coefficients = []
        self.coordinates = []
        self.binary_extended = ""
        self.extended_polynomial = 0
        self.extended_degree = 0
        self.user_input = {}
        self.extra_polynomial = 0

    def initialize(self, num):
        binary = PreProcess().getBinary(num)
        self.chromatic_polynomial = ChromaticPolynomial().getPolynomial(num)
        self.binary_extended = PreProcess().getPerfectString(num)
        self.extra_coefficients = self.getExtraCoefficients(binary)
        self.power = PreProcess().getMatrixDimension(len(self.binary_extended))
        self.extended_polynomial = self.getNewPolynomial()
        self.extended_degree = self.power + len(self.extra_coefficients)
        self.coordinates = self.getCoordinates()

    def getExtraCoefficients(self, binary):
        coefficient_list = []
        length = len(binary)
        if length == 1 or length == 2 or length == 3:
            coefficient_list.append(int(binary, 2))
            return coefficient_list
        start = 0
        end = 2
        while end < length:
            coefficient_list.append(int(binary[start:end + 1], 2))
            start += 3
            end += 3
        if start != length:
            coefficient_list.append(int(binary[start:len(binary)], 2))
        return coefficient_list

    def getNewPolynomial(self):
        x = symbols('x')
        expr = 0
        power = self.power + 1
        for coefficient in self.extra_coefficients:
            expr += coefficient * (x ** int(power))
            power += 1
        self.extra_polynomial = expand(expr)
        new_polynomial = self.extra_polynomial + self.chromatic_polynomial
        print("Extended polynomial = " + str(new_polynomial))
        return new_polynomial

    def getCoordinates(self):
        y_values = []
        x = symbols('x')
        for x_value in range(0, int(self.extended_degree) + 10):
            y_values.append(self.extended_polynomial.subs(x, x_value))
        return y_values

    def lagrangeNumerator(self,):
        x = symbols('x')
        numerator = 1
        for val_x in self.user_input:
            numerator *= (x - int(val_x))
        return numerator

    def lagrangeDenominator(self, curr_x):
        denominator = 1
        for val_x in self.user_input:
            x_here = int(val_x)
            if x_here != curr_x:
                denominator *= (curr_x - x_here)
        return denominator

    def lagrangePolynomial(self):
        x = symbols('x')
        # self.initialize(num)
        lagrange_interpolated_polynomial = 0
        lagrange_numerator = self.lagrangeNumerator()
        end = int(self.extended_degree)
        # print(int(self.power))
        # print(end)
        # print(self.coordinates)
        # if end == len(self.coordinates):
        #     print("equal")
        # print(self.coordinates[end + 1])
        for x_val in self.user_input:
            curr_x = int(x_val)
            curr_y = self.user_input[x_val]
            term = (int(curr_y))*(lagrange_numerator/(x-curr_x)) / self.lagrangeDenominator(curr_x)
            lagrange_interpolated_polynomial += term
        lagrange_interpolated_polynomial = expand(lagrange_interpolated_polynomial)
        # print("Lagrange Interpolated Polynomial = \n" + str(lagrange_interpolated_polynomial))
        return lagrange_interpolated_polynomial

    def retrieve_polynomial(self, lagrange_polynomial):
        x = symbols('x')
        retrieved_chromatic_polynomial = lagrange_polynomial - self.extra_polynomial
        return retrieved_chromatic_polynomial


    def find_cheating(self, lagrange_polynomial):
        x = symbols('x')
        print("Extended Polynomial was = \n" + str(self.extended_polynomial))
        print("\nLagrange Interpolated Polynomial = \n" + str(lagrange_polynomial))
        retrieved_chromatic_polynomial = self.retrieve_polynomial(lagrange_polynomial)
        print("\nRetrieved Chromatic polynomial after removing unnecessary terms = \n" + str(retrieved_chromatic_polynomial))
        print("\nOriginal Chromatic Polynomial = \n" + str(self.chromatic_polynomial))
        if retrieved_chromatic_polynomial == self.chromatic_polynomial:
            print("\n Since Both Polynomials are same , \n So no cheating has been done by user\n")
        else:
            print("\nCheating has been done \n")
        dummy = input("Press Enter to close")

    def solve(self, num):
        x = symbols('x')
        self.initialize(num)
        print("\nFrom the given points on the polynomial : ")
        for i in range(len(self.coordinates)):
            print(" x = " + str(i) + " , y = " + str(self.coordinates[i]))
        print("\n***********  Select any " + str(int(self.extended_degree) + 1) + " points to regenerate the polynomial :  ********\n")
        for i in range(int(self.extended_degree) + 1):
            print(" Select Point Number " + str(i + 1) + " :")
            input_x = input("Enter x co-ordinate : ")
            input_y = input("Enter y co-ordinate : ")
            self.user_input.update({input_x: input_y})
        print("\n********************************************************************************************************\n")
        lagrange_interpolated_polynomial = self.lagrangePolynomial()
        self.find_cheating(lagrange_interpolated_polynomial)



