from scripts.ChromaticPolynomial import *
from sympy import *
from scripts.ModularInverse import *

class SecretSharing:
    def __init__(self):
        self.prime = 97
        self.power = 0
        self.chromatic_polynomial = 0
        self.extra_coefficients = []
        self.coordinates = []
        self.binary_extended = ""
        self.extended_polynomial = 0
        self.extended_degree = 0
        self.user_input = {}
        self.extra_polynomial = 0

    def modInverse(self, a, m):
        for x in range(1, m):
            if (((a % m) * (x % m)) % m == 1):
                return x
        return -1

    def reduced_expr(self, polynomial):
        x = symbols('x')
        # print("Received polynomial = " + str(polynomial))
        # print("Degree = " + str(self.extended_degree))
        res_expr = 0
        res_expr += polynomial.subs(x, 0)
        for i in range(1, int(self.extended_degree) + 1):
            coefficient = polynomial.coeff(x**i)
            # print(print("Current coefficient = " + str(coefficient)))
            coefficient = int(coefficient) % self.prime
            # print("Current coefficient after mod = " + str(coefficient))
            res_expr += coefficient * (x**i)
        return res_expr

    def required_length_of_binary(self):
        return (self.power - 1)*self.power // 2

    def initialize(self, num):
        binary = PreProcess().getBinary(num)
        self.chromatic_polynomial = ChromaticPolynomial().getPolynomial(num)
        self.binary_extended = PreProcess().getPerfectString(num)
        self.extra_coefficients = self.getExtraCoefficients(self.binary_extended)
        self.power = PreProcess().getMatrixDimension(len(self.binary_extended))
        self.extended_degree = self.power + len(self.extra_coefficients)
        self.extended_polynomial = self.getNewPolynomial()
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
            substr = binary[start:end+1]
            print("Substring = " + substr)
            coefficient_list.append(int(substr, 2))
            start += 3
            end += 3
        if start != length:
            coefficient_list.append(int(binary[start:len(binary)], 2))
        return coefficient_list

    def getNewPolynomial(self):
        x = symbols('x')
        expr = 0
        power = self.power + 1
        print("***************************************************")
        print("Used Extra Coefficients are : ")
        print(self.extra_coefficients)
        print("***************************************************")
        for coefficient in self.extra_coefficients:
            expr += coefficient * (x ** int(power))
            power += 1
        self.extra_polynomial = expand(expr)
        new_polynomial = self.extra_polynomial + self.chromatic_polynomial
        # print("Extended polynomial = " + str(new_polynomial))
        result = self.reduced_expr(new_polynomial)
        print("Extended polynomial = " + str(result))
        return result

    def getCoordinates(self):
        y_values = []
        x = symbols('x')
        for x_value in range(0, int(self.extended_degree) + 10):
            y_value = self.extended_polynomial.subs(x, x_value) % self.prime
            y_values.append(y_value)
        return y_values

    def lagrangeNumerator(self):
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
            term = ((int(curr_y) % self.prime) * self.modInverse(self.lagrangeDenominator(curr_x),
                                                                 self.prime))*(expand(lagrange_numerator/(x-curr_x)))
            lagrange_interpolated_polynomial += term
        lagrange_interpolated_polynomial = expand(lagrange_interpolated_polynomial)
        # print("Lagrange Interpolated Polynomial = \n" + str(lagrange_interpolated_polynomial))
        return self.reduced_expr(lagrange_interpolated_polynomial)

    def retrieve_polynomial(self, lagrange_polynomial):
        x = symbols('x')
        retrieved_chromatic_polynomial = lagrange_polynomial - self.extra_polynomial
        return retrieved_chromatic_polynomial

    def int_to_binary(self,coeff):
        return bin(coeff).replace("0b", "")

    def find_cheating(self, lagrange_polynomial):
        x = symbols('x')
        # print("Extended Polynomial was = \n" + str(self.extended_polynomial))
        # print("\nLagrange Interpolated Polynomial = \n" + str(lagrange_polynomial))
        # retrieved_chromatic_polynomial = self.retrieve_polynomial(lagrange_polynomial)
        # print("\nRetrieved Chromatic polynomial after removing unnecessary terms = \n" + str(retrieved_chromatic_polynomial))
        # print("\nOriginal Chromatic Polynomial = \n" + str(self.chromatic_polynomial))
        # if retrieved_chromatic_polynomial == self.chromatic_polynomial:
        #     print("\n Since Both Polynomials are same , \n So no cheating has been done by user\n")
        # else:
        #     print("\nCheating has been done \n")
        # step 1 : extract extra coefficients from interpolated polynomial
        extracted_coefficients = []
        for deg in range(int(self.power)+1, int(self.extended_degree)+1):
            extracted_coefficients.append(lagrange_polynomial.coeff(x**deg))
        print("***************************************************")
        print("Extracted Extra Coefficients are : ")
        print(extracted_coefficients)
        print("***************************************************")
        # step 2 : generate the extended binary string using these coefficients
        extracted_binary = ""
        required_length = self.required_length_of_binary()
        for i in range(0, len(extracted_coefficients) - 1):
            bin_str = self.int_to_binary(extracted_coefficients[i])
            while len(bin_str) < 3:
                bin_str = '0' + bin_str
            extracted_binary += bin_str
        rem_length = required_length - len(extracted_binary)
        last_bin = self.int_to_binary(extracted_coefficients[-1])
        while len(last_bin) < rem_length:
            last_bin = '0' + last_bin
        extracted_binary += last_bin
        print("Extracted binary String = " + extracted_binary)
        extracted_chromatic_polynomial = ChromaticPolynomial().getPolynomialWithString(extracted_binary)
        print("\nRetrieved Chromatic polynomial after processing the secret = \n" +
              str(extracted_chromatic_polynomial))
        print("\nOriginal Chromatic Polynomial = \n" + str(self.chromatic_polynomial))
        if extracted_chromatic_polynomial == self.chromatic_polynomial:
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



