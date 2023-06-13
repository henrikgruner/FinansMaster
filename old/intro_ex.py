import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# Define the parameters
mu = 0.12  # expected return of the portfolio
sigma = 0.20  # volatility of the portfolio
r_f = 0.5  # risk-free rate

# Define a range of time periods
T = np.arange(1, 51)

# Compute the probabilities of underperformance
probs = 1 - norm.cdf((mu - r_f) / sigma * np.sqrt(T))

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(T, probs, label="Probability of Underperformance")
plt.xlabel("Investment horizon (years)")
plt.ylabel("Probability of underperformance (shortfall risk)")
plt.title("Probability of Portfolio Underperforming a Risk-Free Rate Over Time")
plt.grid(True)
plt.legend()
plt.show()
