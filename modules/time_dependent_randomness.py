N = 624
M = 397
MATRIX_A = 0x9908b0df   # constant vector a
UPPER_MASK = 0x80000000  # most significant w-r bits
LOWER_MASK = 0x7fffffff  # least significant r bits

class MT19937:
    def __init__(self, seed):
        self.mt = [0] * N
        self.mti = N + 1
        self.seed_mt(seed)

    def seed_mt(self, seed):
        self.mt[0] = seed & 0xffffffff
        for i in range(1, N):
            self.mt[i] = (1812433253 * (self.mt[i - 1] ^ (self.mt[i - 1] >> 30)) + i) & 0xffffffff

    def extract_number(self):
        if self.mti >= N:
            if self.mti == N + 1:
                self.seed_mt(5489)  # a default initial seed is used

            self.twist()

        y = self.mt[self.mti]
        y ^= (y >> 11)
        y ^= (y << 7) & 0x9d2c5680
        y ^= (y << 15) & 0xefc60000
        y ^= (y >> 18)

        self.mti += 1
        return y & 0xffffffff

    def twist(self):
        for i in range(N):
            y = (self.mt[i] & UPPER_MASK) | (self.mt[(i + 1) % N] & LOWER_MASK)
            self.mt[i] = self.mt[(i + M) % N] ^ (y >> 1)
            if y % 2 != 0:
                self.mt[i] ^= MATRIX_A
        self.mti = 0

def time_dependent_randomness():
    # Initialize with a seed
    seed = 123456789
    mt = MT19937(seed)

    # Generate random numbers
    for _ in range(10):
        print(mt.extract_number())

