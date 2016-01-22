from math import sqrt
from joblib import Parallel, delayed
from time import time


if __name__ == '__main__':
    print("**************************")
    start_time = time()
    [sqrt(i ** 2) for i in range(100000)]
    print("[Done:] %.2f" % (time() - start_time))

    print("**************************")
    start_time = time()
    Parallel(n_jobs=-2)(delayed(sqrt)(i ** 2) for i in range(100000))
    print("[Done:] %.2f" % (time() - start_time))
