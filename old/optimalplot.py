import numpy as np
import matplotlib.pyplot as plt

r_f = 0.05
r_m = 0.12
var = 0.2**2
A_values = [3]  # Different values for A

plt.figure(figsize=(10, 6))

for A in A_values:
    gg = []

    for t in range(0, 51):
        if t == 0:
            upper = r_m + 0.5 * var - r_f
            lower = A * var
        else:
            upper = np.exp((r_m + 0.5 * var) * t) - np.exp(r_f * t)
            lower = A * np.exp((2 * r_m + var) * t) * (np.exp(var * t) - 1)
        gg.append(upper / lower)
        if t % 5 == 0:
            print(t, upper / lower)
        t += 1

    plt.plot(gg, label=f"A = {A}")

plt.title("Optimal allocation in risky assets w.r.t investment horizon")
plt.xticks([x for x in range(0, 51) if x % 5 == 0])
plt.xlabel("Investment horizon (periods)")
plt.ylabel("Proportion of risky asset in portfolio")

plt.grid()
plt.legend()
plt.show()
