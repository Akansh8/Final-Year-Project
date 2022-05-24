import math


class PreProcess:
    def __init__(self):
        self.perfectBits = [0, 1, 3, 6, 10, 15, 21, 28, 36, 45, 55, 66]
    def lower_bound(self,length):
        lo = 0
        hi = len(self.perfectBits) - 1
        ans = -1
        while lo <= hi:
            mid = lo + (hi - lo) // 2
            if self.perfectBits[mid] >= length:
                ans = mid
                hi = mid - 1
            else:
                lo = mid + 1
        return ans
    def getBinary(self,num):
        sol = ""
        while num:
            rem = num % 2
            if rem == 0:
                sol += '0'
            else:
                sol += '1'
            num //= 2
        ans = sol[::-1]
        return ans
    def getPerfectString(self,num):
        bin = self.getBinary(num)
        length = len(bin)
        index = self.lower_bound(length)
        extraBits = self.perfectBits[index] - length
        # print("Extra Bits = " + str(extraBits))
        if extraBits == 0:
            return bin
        pref = (extraBits*"0")
        # print("Prefix of 0s = " + pref)
        return pref + bin

    def getMatrixDimension(self, length):
        dimension = math.sqrt(1 + 8*length) - 1
        return dimension / 2 + 1

    def populate(self, n, binary):
        ptr = 0
        currlen = 1
        matrix = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(1, n):
            for j in range(currlen):
                val = binary[j+ptr]
                if val == '1':
                    matrix[i][j] = 1
            ptr += currlen
            currlen += 1
        i = 1
        while i < n:
            j = 0
            while j < i:
                matrix[j][i] = matrix[i][j]
                j += 1
            i += 1
        return matrix
    def getAdjacencyMatrix(self, num):
        binary = self.getPerfectString(num)
        n = int(self.getMatrixDimension(len(binary)))
        print("Binary String for number = " + binary + "\n")
        print("Vertices in graph = " + str(n) + "\n")
        print("Adjacency Matrix for Graph = ")
        matrix = self.populate(n, binary)
        for row in matrix:
            print(row)
        print("\n")
        return matrix
    def getAdjacencyMatrixWithString(self,binary_string):
        n = int(self.getMatrixDimension(len(binary_string)))
        matrix = self.populate(n, binary_string)
        return matrix


