from form import *

# f = BinaryQuadraticForm(1943, -470, 2166)
# g = f

# i = 1
# while True and i <= 625:
#     print(f"f^{i} = ({g.a}, {g.b}, {g.c})")
#     if g.a == 1:
#         break
#     g *= f
#     i += 1

from primality import primality
import random

prime = 1
while primality.isprime(prime) == False:
    prime = random.randint(100000000, 10000000000)
print(prime)