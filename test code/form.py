from math import gcd, isqrt


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

        a1, b1, c1 = self.a, self.b, self.c
        a2, b2, c2 = other.a, other.b, other.c

        # General composition via CRT / ideal representatives.
        # Choose equivalent forms with coprime leading coefficients.

        f1 = self.reduce()
        f2 = other.reduce()

        a1, b1, c1 = f1.a, f1.b, f1.c
        a2, b2, c2 = f2.a, f2.b, f2.c

        # Find equivalent representative with leading coefficient
        # coprime to a2.
        found = False

        for t in range(-abs(a2), abs(a2) + 1):
            B = b1 + 2 * a1 * t
            A = a1

            if gcd(A, a2) == 1:
                found = True
                break

        if not found:
            raise ArithmeticError(
                "Could not find coprime representatives"
            )

        # Composition when gcd(a1, a2) = 1.
        # Solve B == b1 (mod 2*a1)
        #       B == b2 (mod 2*a2)

        M = 2 * a1
        N = 2 * a2

        g = gcd(M, N)

        if (b2 - B) % g != 0:
            raise ArithmeticError("CRT compatibility failure")

        M1 = M // g
        N1 = N // g

        inv = pow(M1, -1, N1) if N1 > 1 else 0

        k = (((b2 - B) // g) * inv) % N1 if N1 > 1 else 0

        B = B + M * k

        A = a1 * a2
        B = B % (2 * A)

        C = (B**2 - D) // (4 * A)

        result = BinaryQuadraticForm(A, B, C)

        return result.reduce()

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
            f"{self.a}x^2 + {self.b}xy + {self.c}y^2 "
            f"(D={self.discriminant})"
        )