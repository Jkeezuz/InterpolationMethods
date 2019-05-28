import numpy as np

class SplineFunction:
    def __init__(self, z, h, x, y):
        self.z = z
        self.h = h
        self.x = x
        self.y = y
        self.lenx = len(x)

    def get(self, calcx):
        first = np.array([(self.z[i]/6*self.h[i+1])*(self.x[i + 1] - calcx)**3
                          for i in range(self.lenx-2)])
        sec = np.array([(self.z[i + 1]/6*self.h[i+1])*(calcx - self.x[i])**3
                        for i in range(self.lenx-2)])
        th = np.array([(self.y[i+1]/self.h[i+1] - self.z[i+1]*self.h[i+1]/6) * (calcx - self.x[i])
                       for i in range(self.lenx-2)])
        frt = np.array([(self.y[i]/self.h[i+1] - self.z[i]*self.h[i+1]/6) * (self.x[i+1] - calcx)
                        for i in range(self.lenx-2)])
        res = first + sec + th + frt
        return np.sum(res)



class CubicSpline:

    # Implementation based on
    # https://www.math.uh.edu/~jingqiu/math4364/spline.pdf

    def __init__(self, x_values, y_values):
        self.x = np.copy(x_values)
        self.y = np.copy(y_values)
        self.lenx = len(x_values)
        self.m = None
        # Get the distances between points
        self.h = np.diff(x_values)
        # Create the spline
        self.__build_spline()
        self._func = SplineFunction(self.z, self.h, x_values, y_values)

    def get_spline_function(self):
        return self._func

    def __build_spline(self):
        # Create matrix A
        a = self.__build_mat_a()
        d = self.__build_mat_d()
        # Z are the values i of second derivative of Spline in xi
        self.m = np.linalg.solve(a, d)



    def __build_mat_a(self):
        a = np.zeros([self.lenx, self.lenx])
        # Fill the A matrix (page 12 in linked paper)
        a[0][0] = 1.
        a[0][1] = 0.
        a[1][0] = self.h[0]/(self.h[0] + self.h[1])

        for i in range(1, self.lenx-1):
            a[i][i+1] = self.h[i+1]/(self.h[i] + self.h[i+1])
            a[i+1][i] = self.h[i]/(self.h[i] + self.h[i+1])
            a[i][i] = 2

        a[self.lenx - 1][self.lenx-1] = 1
        a[self.lenx - 1][self.lenx-2] = 0
        return a

    def __build_mat_d(self):
        d = np.zeros([self.lenx])
        # Fill the B matrix (page 12 in linked paper)
        #d[0] =
        for i in range(1, self.lenx - 1):
            d[i] = 6*(self.y[i] - self.y[i - 1])/(self.h[i])*(self.h[i]+self.h[i-1])\
                    - 6*(self.y[i - 1] - self.y[i-2])/(self.h[i-1])*(self.h[i]+self.h[i-1])
            return d



    @staticmethod
    def p(x, a, b, c, d):
        return d*x**3 + c*x**2 + b*x + a

    @staticmethod
    def p_d(x, b, c, d):
        return (3 * d * x ** 2) + (2 * c * x) + b

    @staticmethod
    def p_dd(x, c, d):
        return (6 * d * x) + (2 * c)

    def compute(self, calcx):
        x1 = np.where(self.x < calcx)[0][-1]
        x2 = np.where(self.x >= calcx)[0][0]
        calcy = 0

        return calcy




