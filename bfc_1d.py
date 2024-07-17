import numpy as np



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
    itr = 0

    while True:
        dx = - dUdx(x) * dt + np.sqrt(2 * kB * temp * dt) * np.random.rand(0, 1)
        x = x + dx

        if ((x-1.1)**2<1e-3):
            return 1 / (dt * itr)
        
        itr = itr + 1
        
        if itr%100000==0:
            print(itr)



temp = 5000
kB = 8.617333262e-5
dt = 1e-3

rate = ranWalk(temp=temp, dt=dt)
print("Tranistion rate (random walk): %.2e" %rate)

rate_theory = kramers(temp=temp)
print("Transition rate (theory): %.2e" %rate_theory)