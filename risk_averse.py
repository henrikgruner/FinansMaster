import matplotlib.pyplot as plt
import numpy as np

# Define the wealth range
wealth = np.linspace(1, 10, 100)

# Define the utility functions
def utility_risk_averse(x):
    return np.sqrt(x)

def utility_risk_neutral(x):
    return x

def utility_risk_loving(x):
    return x**2

# Calculate utilities
utility_averse = utility_risk_averse(wealth)
utility_neutral = utility_risk_neutral(wealth)
utility_loving = utility_risk_loving(wealth)

# Create the plot
plt.figure(figsize=(8,6))
plt.plot(wealth, utility_averse, label='Risk Averse: U(x) = sqrt(x)', linewidth=2)
plt.plot(wealth, utility_neutral, label='Risk Neutral: U(x) = x', linewidth=2)
plt.plot(wealth, utility_loving, label='Risk Loving: U(x) = x^2', linewidth=2)
plt.legend(loc='upper left')
plt.xlabel('Wealth')
plt.ylabel('Utility')
plt.title('Utility Functions for Different Risk Preferences')
plt.grid(True)
plt.show()
