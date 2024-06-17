import matplotlib.pyplot as plt
def time_dependent_randomness():
    print("time_dependent_randomness algorithm")


class lcgRandomGenerator:
    def __init__(self, seed):
        super().__init__()
        self.initVal = int(seed)

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

    def lcg(self, modulus=2 ** 31 - 1, multiplier=16807, increment=0, startingval=1):
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
        assert (fun == self.lcg)
        randlist = []  # Create an empty list to populate
        for ind in range(num):
            val = fun(modulus, multiplier, increment, initval)
            initval = val  # Set the previous random number as the new seed
            randlist.append(val)  # Append to the list
        return randlist

    def spectraltest(self, fun=None, modulus=256, multiplier=21, increment=11, startingval=0, num=512, t=2,
                     filename='spectral_test.png'):
        if fun is None:
            fun = self.lcg
        randlist = self.lcgrandom(fun, modulus, multiplier, increment, startingval, num)
        x = randlist[0::2]
        y = randlist[1::2]
        plt.figure()  # Create a new figure
        plt.plot(x, y, 'b.')
        plt.axis('square')
        plt.axis('tight')
        plt.savefig(filename)
        plt.close()  # Close the figure

    def randint(self, a, b):
        """ return random int in [a,b) """
        n = self.lcg(startingval=self.initVal)
        self.initVal = n
        return int(n % (b - a) + a)

    def sample(self, obj, amount):
        assert(len(obj) > amount)
        lenght = len(obj)
        samples = []
        randInts = []
        n = self.randint(0,len(obj))

        for i in range(amount):
            while n in randInts:
                n = self.randint(0,len(obj))
            randInts.append(n)
            samples.append(obj[n])

        return samples



