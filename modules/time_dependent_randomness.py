import sys
import numpy as np
import matplotlib.pyplot as plt

def time_dependent_randomness():
    print("time_dependent_randomness algorithm")


class lcgRandomGenerator:
    def __init__(self):
        super().__init__()

    def modulosum(self, x, y, m):
        assert (x >= 0 and y >= 0)
        assert (x <= m - 1 and y <= m - 1)
        assert (type(x) == int)
        assert (type(y) == int)
        assert (type(m) == int)

        if x <= m - 1 - y:
            return x + y
        else:
            return x - (m - y)

    def lcg1(self, modulus=2 ** 31 - 1, multiplier=16807, increment=0, startingval=1):
        # Check conditions
        assert (modulus >= 1)
        assert (multiplier >= 0 and increment >= 0 and startingval >= 0)
        assert (multiplier <= modulus - 1 and increment <= modulus - 1 and startingval <= modulus - 1)
        assert (multiplier <= sys.maxsize / (modulus - 1))
        # Algorithm 1
        r = (multiplier * startingval) % modulus
        r = self.modulosum(r, increment, modulus)
        return r

    def lcg2(self, modulus=2 ** 31 - 1, multiplier=16807, increment=0, startingval=1):
        # Check conditions
        assert (modulus >= 1)
        assert (multiplier >= 0 and increment >= 0 and startingval >= 0)
        assert (multiplier <= modulus - 1 and increment <= modulus - 1 and startingval <= modulus - 1)
        assert ((modulus % multiplier) <= (modulus / multiplier))
        # Algorithm 2
        q = modulus // multiplier
        p = modulus % multiplier
        r = multiplier * (startingval % q) - p * (startingval // q)
        if r < 0:
            r += modulus
        r = self.modulosum(r, increment, modulus)
        return r

    def lcgrandom(self, fun=None, modulus=2 ** 32 - 1, multiplier=367, increment=314, initval=1, num=10):
        if fun is None:
            fun = self.lcg2
        # Check conditions
        assert (fun == self.lcg1 or fun == self.lcg2)
        randlist = []  # Create an empty list to populate
        for ind in range(num):
            val = fun(modulus, multiplier, increment, initval)
            initval = val  # Set the previous random number as the new seed
            randlist.append(val)  # Append to the list
        return np.array(randlist)

    def spectraltest(self, fun=None, modulus=256, multiplier=21, increment=11, startingval=0, num=512, t=2,
                     filename='spectral_test.png'):
        if fun is None:
            fun = self.lcg2
        randlist = self.lcgrandom(fun, modulus, multiplier, increment, startingval, num)
        x = randlist[0::2]
        y = randlist[1::2]
        plt.figure()  # Create a new figure
        plt.plot(x, y, 'b.')
        plt.axis('square')
        plt.axis('tight')
        plt.savefig(filename)
        plt.close()  # Close the figure

