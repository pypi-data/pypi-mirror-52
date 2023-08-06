import math
import matplotlib.pyplot as plt

class Matrix:
    ''' Creation of a class of matrix which enables to make some computations: add,
    substract, multiplication, inverse'''
    
    def __init__(self, n, p):
        '''Method for initializing an object matrix:
            Args:
            n: number of lines
            p: number of columns
            '''
        self.n = n
        self.p = p
        mat = []
        for i in range n:
            ligne=[]
            for j in range p:
                ligne.append(0)
            mat.append(ligne)
        self.matrix = mat
       
    def load(self,array): #Convert a 2D array in a matrix
        if len(array) != self.n or len(array[0]) != self.n:
            return ("error : Bad dimensions")
        for i in range(self.nl):
            for j in range(self.nc):
                self.matrix[i][j]=array[i][j]
                
    def add (self, other):
        if (self.n != other.n or self.p != other.p):
            return ("Error: You must add matrix with same dimensions")
        else:
            mat= matrix(n, p)
            for i in range len(self.n):
                for j in range len(self.p):
                    mat[i][j]= self[i][j] + other[i][j]
        return mat
    
    def sub(self,other):
        (self.n != other.n or self.p != other.p):
            return ("error : You must add same dimension matrix")
        matreturn = matrix(self.n,self.p)
        for i in range(self.n):
            for j in range(self.p):
                matreturn[i][j]=self[i][j]-other[i][j]
        return matreturn
    
    
   def multiply(self, other):
    if (self.p != other.n):
        retrun('Bad dimensions')
    else:
        matc=matrix(self.n, other.p)
        for i in range (self.n):
            for j in range (other.p):
                for k in range self.p:
                    matc[i][j] += self[i][k]*other[k][j]
    return matc
    
    
    def pow(self, m):
        if self.n != self.np:
            return ("error : you must use a square matrix")
        if m == 0:
            matreturn= matrix(self.n, self.p)
            matreturn.identity()
            return matreturn
        if m>0:
            matreturn= matrix(self.n, self.p)
            matreturn.identity()
            for i in range m:
                matreturn = matreturn * self
            return matreturn
        if m==-1:
            return ("error : you must inverse the matrix with the function inverse")
        if m<-1:
            return ("error : you must inverse the matrix with the function inverse")
        
       
        


            
                
            
            
        
                    
        
        