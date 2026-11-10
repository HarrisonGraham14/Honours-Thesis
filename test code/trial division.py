import math
import time

N = 8885488699 * 4484488903

t_start = time.time()

for i in range(2, math.floor(math.sqrt(N))):
    if N % i == 0:
        print(f"{N} = {i} * {N // i}")
        break

t_finish = time.time()
print(f"time: {t_finish - t_start}")