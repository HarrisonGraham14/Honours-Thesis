import math

def extendedEuclid(basis: list[int]):
    pass

class Form:
    a: int
    b: int
    c: int
    Disc: int

    def __init__(self, a: int, b: int, c: int):
        self.a = a
        self.b = b
        self.c = c
        self.Disc = (b * b) - (4 * a * c)

    # Composition
    def __mul__(self, other: Form):
        assert self.Disc == other.Disc
        B = (self.b + other.b) // 2
        coeffs, n = extendedEuclid(self.a, other.a, B)
        m = (self.a * other.b * coeffs[0]) + (self.b * other.a * coeffs[1]) + (((self.b * other.b) + self.Disc) * coeffs[2] // 2)
        return Form(
            (self.a * other.a) // (n * n),
            m // n,
            ((m * m) - (n * n * self.Disc)) // (self.a * other.a)
        )

    def isReduced(self):
        if (self.a == math.abs(self.b)) or (self.a == self.c):
            return self.b >= 0
        return (math.abs(self.b) <= self.a <= self.c)

    def reduce(self):
        while self.isReduced() == False:

            # T Step
            k = math.ceil((self.b - self.a) / (2 * self.a))
            self.c = (k * k * self.a) + (k * self.b) + self.c
            self.b = (2 * k * self.a) + self.b

            # S Step
            if (self.a > self.c) or ((self.a == self.c) and self.b < 0):
                self.a, self.c = self.c, self.a
                self.b *= -1