import math
import random
from primality import primality
from form import PositiveDefiniteForm

# algorithm for finding modular square root
def modSqrt(a, p):
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

# Baby Step Giant Step algorithm
def BSGS(f: PositiveDefiniteForm):

    # bound on the class number
    H = math.ceil(math.sqrt(abs(f.discriminant)) * (math.log(abs(f.discriminant)) + 2) / math.pi)

    # baby steps
    b = f
    babySteps = { str(b) : 1 }
    for i in range(2, math.ceil(math.sqrt(H)) + 1):
        b *= f
        if b.a == 1:
            return i
        babySteps[str(b)] = i

    # giant steps
    G = PositiveDefiniteForm(b.a, -b.b, b.c)
    g = G
    for i in range(1, math.ceil(math.sqrt(H)) + 1):
        if str(g) in babySteps.keys():
            return babySteps[str(g)] + math.ceil(math.sqrt(H)) * i
        g *= G

# fast powering algorithm        
def fastPower(f: PositiveDefiniteForm, d: int):
    g = f
    h = PositiveDefiniteForm.Identity(f.discriminant)
    for i in range(math.ceil(math.log2(d)) + 1):
        if (d >> i) % 2 == 1:
            h *= g
        g = g * g
    return h



def factor_ambiguousForms(N: int):
    
    # ensure N is positive
    N = abs(N)

    # ensure N is odd
    if N % 2 == 0:
        return 2

    # ensure N is composite
    if primality.isprime(N):
        return None

    # choose the appropriate discriminant
    D = -N if -N % 4 == 1 else -4 * N

    # we keep a log of forms with degree 4 which square to an ambiguous form giving a trivial factorisation
    trivialSqrts = []

    # sample primes until a factorisation is found
    while True:
        p = 1
        while not primality.isprime(p):
            p = random.randint(2, abs(D))

        # find b which squares to D mod p (if it exists)
        b = modSqrt(D, p)
        if b == None:
            continue

        # we get a non-primitive form only when p divides D, but in this case, we have factored D
        if D % p == 0:
            return p

        # compute the corresponding form and its order
        if (b * b - D) % (4 * p) != 0:
            continue
        f = PositiveDefiniteForm(p, b, (b * b - D) // (4 * p))
        d = BSGS(f)

        # if d is even compute the corresponding ambiguous form
        if d % 2 != 0:
            continue
        g = fastPower(f, d // 2)

        # extract a factor from the ambiguous form
        x = (2 * g.a) - g.b if g.a == g.c else g.a
        if not x in [1, 2, 4, D, 2 * D, 4 * D]:
            return x

        # if the factorisation is trivial, check if we found a square root of the trivial ambiguous form
        if d % 4 != 0:
            continue
        h1 = fastPower(f, d // 4)

        # if this is the first time we have seen this square root, multiply it with other square roots to find a (hopefully nontrivial) ambiguous form
        if h1 in trivialSqrts:
            continue
        for h2 in trivialSqrts:
            g = h1 * h2.inverse()
            x = (2 * g.a) - g.b if g.a == g.c else g.a
            if not x in [1, 2, 4, D, 2 * D, 4 * D]:
                return x
        trivialSqrts.append(h1)