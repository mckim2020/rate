import numpy as np
import multiprocessing as mp 
from functools import partial
import time
import matplotlib.pyplot as plt


def U(x):
    return 4/3*x**4 - 10/3*x**2 + 2

def dUdx(x):
    return 16/3*x**3 - 20/3*x



def kramers(temp):
    kB = 8.617333262e-5
    factor = 1.5005271936

    return factor * np.exp(-2.08333333333 / kB / temp)



def ranWalk(temp, dt):
    x = -1.1
    kB = 8.617333262e-5
    itr = 0
    noises = np.random.normal(0, 1, int(1e6))
    while True:
        dx = - dUdx(x) * dt + np.sqrt(2 * kB * temp * dt) * noises[itr%int(1e6)]
        x = x + dx

        if ((x-1.1)**2<1e-3):
            return dt * itr
        
        itr = itr + 1
        
        # if itr%100000==0:
        #     print(itr)


if __name__ == "__main__":
    temp = 7000
    kB = 8.617333262e-5
    dt = 1e-4
    count_max = 1000
    serial = False
    fpt = 0
    temp_list = [1000*i for i in range(5,11)]
    RW = []
    Theory = []
    for temp in temp_list:
        tic = time.perf_counter()
        if serial:
            for _ in range(count_max):
                fpt = fpt + ranWalk(temp, dt)

            fpt = fpt / count_max
        else:
            pool = mp.Pool(mp.cpu_count())
            calc_fpt = partial(ranWalk, dt = dt)
            res = pool.map(calc_fpt,[temp for i in range(count_max)])
            pool.close()
            pool.join()
            fpt = np.mean(res)
        toc = time.perf_counter()
        print(f'Time taken for {temp} K is {toc-tic} s')
        rate = 1.0/fpt
        RW.append(rate)
        print(f"Tranistion rate at {temp} K (random walk): {rate}")
        '''
        rate = ranWalk(temp=temp, dt=dt)
        print("Tranistion rate (random walk): %.2e" %rate)
        '''
        rate_theory = kramers(temp=temp)
        Theory.append(rate_theory)
        print(f"Transition rate at {temp} K (theory): {rate_theory}")

    plt.semilogy(1.0/np.array(temp_list), np.array(RW), 'ro', label='RW')
    plt.semilogy(1.0/np.array(temp_list), np.array(Theory), 'k:', label='Theory')
    # plt.yscale('log')
    plt.legend()
    plt.show()
