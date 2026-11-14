import time
import random
from primality import primality
import multiprocessing
import matplotlib.pyplot as plt

def randomPrime(digits):
    p = 1
    while primality.isprime(p) == False:
        p = random.randint(10**(digits - 1), 10**digits)
    return p

def timeAlgorithm(algorithm, args, queue):
    t_start = time.time()
    algorithm(*args)
    t_end = time.time()
    queue.put(t_end - t_start)

def plotAsymptotics(algorithm, maxTime = 3600, samplesPerStep = 3, printLogs = True):
    t_start = time.time()

    # axes for plot
    digits_values = []
    time_values = []

    # loop factoring the product of two D-digit primes
    digits = 0
    while time.time() - t_start < maxTime:
        digits += 1
        if printLogs:
            print(f"\nFactoring product of primes with {digits} digits")

        samples = []
        for _ in range(samplesPerStep):
            p1 = randomPrime(digits)
            p2 = randomPrime(digits)
            N = p1 * p2
            if printLogs:
                print(f"Factoring {p1} * {p2}... ", end="")

            queue = multiprocessing.Queue()
            process = multiprocessing.Process(target = timeAlgorithm, args = (algorithm, (N,), queue))
            process.start()
            process.join(maxTime - (time.time() - t_start))
            if not process.is_alive():
                sampleTime = queue.get()
                samples.append(sampleTime)
                if printLogs:
                    print(f"finished in {sampleTime}s")
            else:
                if printLogs:
                    print(f"not finished")
                break

        if (len(samples) > 0):
            avgTime = sum(samples) / len(samples)
            digits_values.append(digits)
            time_values.append(avgTime)
            if printLogs:
                print(f"Average time: {avgTime}s")

    print(f"\nx-axis: digits_values = {digits_values}")
    print(f"y-axis: time_values = {time_values}")

    plt.plot(digits_values, time_values, "ko")
    plt.show()



from factor_trialDivision import factor_trialDivision
from factor_ambiguousForms import factor_ambiguousForms
if __name__ == "__main__":
    # plotAsymptotics(factor_trialDivision)
    plotAsymptotics(factor_ambiguousForms)