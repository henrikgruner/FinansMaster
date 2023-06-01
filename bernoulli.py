import numpy as np
from scipy.optimize import newton
import matplotlib.pyplot as plt

def f(x, w, N=50):
    series_sum = sum([(1/2)**(n) * np.log(2**(n-1) + w) for n in range(1, N+1)])
    return np.log(w + x) - series_sum

w_values = np.arange(100, 100001, 100)
x_values = [newton(f, 0, args=(w,)) for w in w_values]

plt.plot(w_values, x_values)
plt.xlabel("Wealth (w)")
plt.ylabel("Amount to Pay to Enter the Game ($\zeta$)")
plt.title("Amount to Pay to Enter the St. Petersburg Game vs Wealth Level")
plt.grid(True)
plt.show()
