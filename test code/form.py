from math import gcd, isqrt

def gcdExtended(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = gcdExtended(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

class BinaryQuadraticForm:

    def __init__(self, a, b, c):
        self.a = int(a)
        self.b = int(b)
        self.c = int(c)

        self.discriminant = self.b**2 - 4*self.a*self.c

        self._validate()

    def _validate(self):
        if self.a <= 0:
            raise ValueError("a must be positive")

        if self.discriminant >= 0:
            raise ValueError("Discriminant must be negative")

        if self.discriminant % 4 not in (0, 1):
            raise ValueError("Invalid quadratic form discriminant")

        if gcd(gcd(abs(self.a), abs(self.b)), abs(self.c)) != 1:
            raise ValueError("Form must be primitive")

    def is_reduced(self):
        return (
            abs(self.b) <= self.a <= self.c
            and not (
                (abs(self.b) == self.a or self.a == self.c)
                and self.b < 0
            )
        )

    def is_ambiguous(self):
        f = self.reduce()
        return (f.b == 0) or (f.a == f.b) or (f.a == f.c)

    def reduce(self):
        a, b, c = self.a, self.b, self.c

        while True:

            # Ensure a <= c
            if a > c:
                a, b, c = c, -b, a

            # Reduce b into the interval [-a, a]
            m = (a - b) // (2 * a)

            b_new = b + 2 * a * m
            c_new = (b_new**2 - self.discriminant) // (4 * a)

            b, c = b_new, c_new

            # Apply boundary convention
            if abs(b) <= a <= c:
                if (abs(b) == a or a == c) and b < 0:
                    b = -b

                return BinaryQuadraticForm(a, b, c)

    def __mul__(self, other):

        if not isinstance(other, BinaryQuadraticForm):
            return NotImplemented

        if self.discriminant != other.discriminant:
            raise ValueError(
                "Forms must have the same discriminant"
            )

        D = self.discriminant

        f1 = self.reduce()
        f2 = other.reduce()

        a1, b1, c1 = f1.a, f1.b, f1.c
        a2, b2, c2 = f2.a, f2.b, f2.c

        B = (b1 + b2) // 2

        n1, u1, v1 = gcdExtended(a1, a2)
        n, z, w = gcdExtended(n1, B)
        u = z * u1
        v = z * v1

        m = (a1 * b2 * u) + (a2 * b1 * v) + (((b1 * b2) + D) * w // 2)

        a = a1 * a2 // (n**2)
        b = m // n
        c = (m**2 - ((n**2) * D)) // (4 * a1 * a2)

        result = BinaryQuadraticForm(a, b, c)
        result = result.reduce()

        return result

    def __eq__(self, other):
        if not isinstance(other, BinaryQuadraticForm):
            return False

        return (
            self.a == other.a
            and self.b == other.b
            and self.c == other.c
        )

    def __repr__(self):
        return (
            f"BinaryQuadraticForm("
            f"a={self.a}, b={self.b}, c={self.c}, "
            f"D={self.discriminant})"
        )

    def __str__(self):
        return (
            f"({self.a}, {self.b}, {self.c})"
        )