import math

def factor_trialDivision(N: int):

    # we need only check divisibility by 2, 3, and numbers which are 1 or 5 (mod 6)
    for i in [2, 3, 5]:
        if N % i == 0:
            return i

    for i in range(1, math.floor(math.sqrt(N) / 6)):
        if N % (6 * i + 1) == 0:
            return N % (6 * i + 1)
        if N % (6 * i + 5) == 0:
            return N % (6 * i + 5)