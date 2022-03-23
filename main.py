from scripts.ChromaticPolynomial import *
from scripts.SecretSharing import *
# adjMat = PreProcess().getAdjacencyMatrix(2)


num = input("enter an integer : ")
print("\nEntered Number = " + str(num) + "\n")
SecretSharing().solve(int(num))