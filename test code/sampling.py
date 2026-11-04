from random import randint
from form import *

def randomLattice(Disc: int):

    # ideal generators, of the form x + ((Disc + sqrtDisc) / 2)y
    gen_1 = [ randint(1, 2**32), randint(1, 2**32) ]
    gen_2 = [ randint(1, 2**32), randint(1, 2**32) ]

    # additional Z-module generators, obtained by multiplying by (Disc + sqrtDisc) / 2
    gen_3 = [ (Disc * (1 - Disc) // 4) * gen_1[1], gen_1[0] + (Disc * gen_1[1]) ]
    gen_4 = [ (Disc * (1 - Disc) // 4) * gen_2[1], gen_2[0] + (Disc * gen_2[1]) ]

    # reduce to HNF
    