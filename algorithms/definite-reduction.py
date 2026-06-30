import numpy as np

def ReducePositiveDefinite(a, b, c):
    while np.abs(b) > a or a > c:
        
        # Step 1: T reduction
        if np.abs(b) > a:
            k = -np.floor(b / a)
            c = a * k * k + b * k + c
            b = 2 * a * k + b

        # Step 2: S reduction
        if a > c:
            a, b, c = c, -b, a
    
    # Step 3: special cases require b > 0
    if a == abs(b) or a == c:
        if b < 0:
            a, b, c = c, -b, a

    return a, b, c