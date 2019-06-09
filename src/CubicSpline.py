import numpy as np


class CubicSpline:

    u''' Cubic spline interpolation implementation.
    Based on: http://fourier.eng.hmc.edu/e176/lectures/ch7/node6.html
    All numbers in parentheses correspond to the numbers in parentheses
    on the right hand side of math formulas visible in the linked paper.
    It allows for easier understanding of code and the correlation between it
     and the math formulas'''


    def __init__(self, x_values, y_values):
        self.x = np.copy(x_values)
        self.y = np.copy(y_values)
        self.lenx = len(x_values)
        self.m = None
        # Get the distances between points
        # IMPORTANT!!
        ''' h[i] in paper = x[i] - x[i-1]
            h[i] in this code = x[i+1] - x[i]'''
        self.h = np.diff(x_values)
        # Create the spline
        self.__build_spline()

    def __build_spline(self):
        # Create matrix A (98), the left hand side matrix
        A = self.__build_mat_a()
        # Create vector D (98), the right hand side vector
        D = self.__build_mat_d()
        # Solve the linear equation for M vector in (98)
        self.M = np.linalg.solve(A, D)

        # Calculate c and d coefficients
        # Using (82) and (83)
        self.c = np.array([])
        self.d = np.array([])
        for i in range(len(self.M)-1):
            res = (self.y[i+1] - self.y[i])/self.h[i] - (self.h[i]*(self.M[i+1] - self.M[i]))/6
            self.c = np.append(self.c, res)

            res = (self.x[i+1]*self.y[i] - self.x[i]*self.y[i+1])/self.h[i]\
                  - (self.h[i]*(self.x[i+1]*self.M[i] - self.x[i]*self.M[i+1])/6)
            self.d = np.append(self.d, res)
        print("")




    def __build_mat_a(self):
        # We assume that f''(x0) and f''(xn) are known and equal 0
        # Then we can create the matrix on left hand side of (98)
        a = np.zeros([self.lenx, self.lenx])
        a[0][0] = 1.
        for i in range(1, len(self.h)):
            u = self.h[i-1]/(self.h[i-1] + self.h[i])
            a[i][i-1] = u
            a[i][i+1] = 1-u
            a[i][i] = 2
        a[-1][-1] = 1
        return a

    def __build_mat_d(self):
        # We assume that f''(x0) and f''(xn) are known and equal 0
        # Then we can create the vector on right hand side of (98)
        d = np.zeros([self.lenx])
        for i in range(1, len(self.h)):
            d[i] = 6*(self.y[i+1] - self.y[i])/((self.h[i])*(self.h[i]+self.h[i-1]))\
                    - 6*(self.y[i] - self.y[i-1])/((self.h[i-1])*(self.h[i]+self.h[i-1]))
        d[-1] = 0
        d[0] = 0
        return d



    def _calculate(self, x, i):
        # Calculate the value y for x in our interpolated function
        # Using (80)
        return self.M[i-1]*((self.x[i] - x)**3)/(6*self.h[i-1]) +\
               self.M[i]*((x - self.x[i-1])**3)/(6*self.h[i-1]) + \
               self.c[i-1]*x + self.d[i-1]

    def get(self, calcx):
        # Find the section in which calcx lies and calculate the value y for calcx
        if calcx < int(self.x[0]):
            return None
        elif calcx > int(self.x[-1]):
            return None
        if calcx not in self.x:
            idx = np.where(self.x > calcx)[0][0]
        else:
            idx = np.where(self.x == calcx)[0] + 1

        calcy = self._calculate(calcx, idx)

        return calcy




