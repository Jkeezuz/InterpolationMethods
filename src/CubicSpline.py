import numpy as np


class CubicSpline:

    def __init__(self, x_values, y_values):
        self.x = np.copy(x_values)
        self.y = np.copy(y_values)
        self.lenx = len(x_values)
        self.m = None
        # Get the distances between points
        self.h = np.diff(x_values)
        # Create the spline
        self.__build_spline()

    def __build_spline(self):
        # Create matrix A
        a = self.__build_mat_a()
        dres = self.__build_mat_d()
        # M are the values i of second derivative of Spline in xi
        self.M = np.linalg.solve(a, dres)

        #Calculate c and d coefficients
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
        d = np.zeros([self.lenx])

        for i in range(1, len(self.h)):
            d[i] = 6*(self.y[i+1] - self.y[i])/((self.h[i])*(self.h[i]+self.h[i-1]))\
                    - 6*(self.y[i] - self.y[i-1])/((self.h[i-1])*(self.h[i]+self.h[i-1]))
        d[-1] = 0
        d[0] = 0
        return d



    def _calculate(self, x, i):
        return self.M[i-1]*((self.x[i] - x)**3)/(6*self.h[i-1]) +\
               self.M[i]*((x - self.x[i-1])**3)/(6*self.h[i-1]) + \
               self.c[i-1]*x + self.d[i-1]

    def get(self, calcx):
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




