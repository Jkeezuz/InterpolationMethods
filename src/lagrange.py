import numpy as np
# Lagrange interpolation
# Get a value of lagrange interpolation in x for known x_values and y_values
def lagrange(x, x_values, y_values):
    def _base(j):
        dividend = np.delete(x_values, j)

        divisor = np.copy(dividend)

        dividend = x - dividend
        dividend = np.prod(dividend)
        if dividend == -np.inf or dividend == np.inf:
            return dividend

        divisor = x_values[j] - divisor
        divisor = np.prod(divisor)
        if divisor == -np.inf or divisor == np.inf:
            return 0

        res = dividend/divisor
        return res

    base = np.array([_base(k) for k in range(len(y_values))])
    return np.sum(base * y_values)

