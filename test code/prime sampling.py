from primality import primality
import random
from form import *
import time

discriminant = - 4 * 8885488699 * 4484488903

def mod_sqrt(a, p):
    """
    Compute a square root of a modulo an odd prime p.
    Returns x such that x^2 = a (mod p), or None
    if no square root exists.
    """
    a %= p

    if a == 0:
        return 0

    # Check whether a is a quadratic residue
    if pow(a, (p - 1) // 2, p) != 1:
        return None

    # Shortcut when p = 3 (mod 4)
    if p % 4 == 3:
        return pow(a, (p + 1) // 4, p)

    # Factor p - 1 = q * 2^s, with q odd
    q = p - 1
    s = 0
    while q % 2 == 0:
        s += 1
        q //= 2

    # Find a quadratic non-residue z
    z = 2
    while pow(z, (p - 1) // 2, p) != p - 1:
        z += 1

    # Initialize
    m = s
    c = pow(z, q, p)
    t = pow(a, q, p)
    r = pow(a, (q + 1) // 2, p)

    while t != 1:
        # Find smallest i such that t^(2^i) = 1
        i = 1
        temp = (t * t) % p
        while temp != 1:
            temp = (temp * temp) % p
            i += 1

        # Update
        b = pow(c, 1 << (m - i - 1), p)
        m = i
        c = (b * b) % p
        t = (t * c) % p
        r = (r * b) % p

    return r


import math

def BSGS(form: BinaryQuadraticForm, bound):
    B = form
    b = B
    babySteps = { str(b) : 1 }
    for i in range(2, math.ceil(math.sqrt(bound)) + 1):
        b *= B
        if b.a == 1:
            return i
        babySteps[str(b)] = i

    G = BinaryQuadraticForm(b.a, -b.b, b.c)
    g = G
    for i in range(1, math.ceil(math.sqrt(bound)) + 1):
        if str(g) in babySteps.keys():
            return babySteps[str(g)] + math.ceil(math.sqrt(bound)) * i
        g *= G

    return None
        
def fast_power(element, exponent):
    if exponent < 0:
        raise ValueError("Exponent must be non-negative")

    if exponent == 0:
        raise ValueError("Provide an identity element for exponent zero")

    # Generate powers: A, A^2, A^4, A^8, ...
    powers = []
    current = element

    tempexponent = exponent
    while tempexponent:
        powers.append(current)
        current = current * current
        tempexponent >>= 1

    # Multiply selected powers together
    result = None

    for i, power in enumerate(powers):
        if (exponent >> i) & 1:
            result = power if result is None else result * power

    return result

t_start = time.time()

done = False
while done == False:
    samplePrime = 1
    while not primality.isprime(samplePrime):
        samplePrime = random.randint(2, abs(discriminant))

    b = mod_sqrt(discriminant, samplePrime)

    if b == None:
        continue

    if (b**2 - discriminant) % (4 * samplePrime) == 0:
        print(f"sample prime: {samplePrime}")
        c = (b**2 - discriminant) // (4 * samplePrime)
        f = BinaryQuadraticForm(samplePrime, b, c).reduce()

        order = BSGS(f, 2 * math.ceil(math.sqrt(abs(discriminant))))
        if order % 2 == 0:
            g = fast_power(f, order // 2)
            print(f"{f}^{order // 2} = {g}")
            if g.a > 4:
                done = True
        else:
            g = fast_power(f, order)
            print(f"{f}^{order} = {g}")
        print()

t_finish = time.time()
print(f"time: {t_finish - t_start}")