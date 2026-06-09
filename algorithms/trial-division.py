import numpy as np

def factor(n):
    for x in range(2, int(np.sqrt(n)) + 1):
        if n % x == 0: 
            return x