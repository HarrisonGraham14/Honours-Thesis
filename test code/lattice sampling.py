from sympy import Matrix
from sympy.matrices.normalforms import hermite_normal_form
import math
import random
random.seed()

def lattice_basis(vectors):

    if not vectors:
        raise ValueError("Input list cannot be empty")

    # Vectors are columns of the matrix
    M = Matrix.hstack(
        *[Matrix(v) for v in vectors]
    )

    # Compute column Hermite Normal Form
    H = hermite_normal_form(M)

    if H.cols != 2:
        raise ValueError("The lattice does not have rank 2")

    return [
        (int(H[0, 0]), int(H[1, 0])),
        (int(H[0, 1]), int(H[1, 1]))
    ]


def randomLattice(discriminant):
    random_vector_1 = (random.randint(1, abs(discriminant)), 0)
    random_vector_2 = (random.randint(1, abs(discriminant)), random.randint(1, abs(discriminant)))

    vectors = [
        random_vector_1,
        (0, random_vector_1[0]),
        random_vector_2,
        (random_vector_2[1] * ((discriminant - (discriminant**2)) // 4), random_vector_2[0] + discriminant * random_vector_2[1])
    ]

    basis = lattice_basis(vectors)
    return basis


from form import *

discriminant = - 4 * 1187 * 3499
tally = {}
ambiguous = {}

for i in range(10000):
    basis = randomLattice(discriminant)
    l = basis[0][0]
    m = (2 * basis[1][0]) + (basis[1][1] * discriminant)
    n = basis[1][1]
    f = BinaryQuadraticForm(l // n, m // n, (m**2 - n**2 * discriminant) // (4 * l * n))
    f = f.reduce()
    key = f"({f.a}, {f.b}, {f.c})"
    if not key in tally.keys():
        tally[key] = 0
        g = BinaryQuadraticForm(f.a, f.b, f.c)
        half_order = 1
        while g.is_ambiguous() == False:
            g *= f
            g = g.reduce()
            half_order += 1
        ambiguous[key] = f"^{half_order} = ({g.a}, {g.b}, {g.c})"
    tally[key] += 1

for key in tally.keys():
    print(f"{key} : {ambiguous[key]}")