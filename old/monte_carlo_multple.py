import datetime
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from datasets import get_datasets, get_shiller
import matplotlib.pyplot as plt


data = get_datasets('1980')

print(data)


def utility_function(weights, returns_market, returns_rf, volatility_market, risk_aversion):
    portfolio_return = weights[0] * returns_market + weights[1] * returns_rf
    portfolio_volatility = weights[0] * volatility_market
    portfolio_variance = portfolio_volatility**2
    utility = np.mean(portfolio_return) - risk_aversion * np.mean(portfolio_variance)
    return -utility

# The previous code remains unchanged until the monte_carlo_simulation function

def monte_carlo_simulation(data, risk_aversion, num_simulations=10000):
    np.random.seed(42)
    optimal_weights = None
    max_utility = float('-inf')
    
    # Initialize arrays to store utilities and corresponding weights
    utilities = []
    weights_list = []
    
    for i in range(num_simulations):
        weights = np.random.dirichlet(np.ones(2), size=1).flatten()
        utility = -utility_function(weights, data['returns'], data['returns_rf'], data['volatility_market'], risk_aversion)
        
        # Store utilities and weights
        utilities.append(utility)
        weights_list.append(weights)
        
        if utility > max_utility:
            max_utility = utility
            optimal_weights = weights
            
    return optimal_weights, max_utility, utilities, weights_list

risk_aversions = np.arange(1, 4.5, 0.5)
optimal_market_weights = []

for risk_aversion in risk_aversions:
    optimal_weights, max_utility, utilities, weights_list = monte_carlo_simulation(data, risk_aversion)
    optimal_market_weights.append(optimal_weights[0])

# Plot the optimal market weights for different risk aversion levels
plt.plot(risk_aversions, optimal_market_weights, marker='o', linestyle='-')
plt.xlabel('Risk Aversion')
plt.ylabel('Optimal Market Asset Weight')
plt.title('Optimal Market Asset Weight for Different Risk Aversions')
plt.grid()
plt.show()


risk_aversions = np.arange(1, 4.5, 0.5)
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

fig, ax = plt.subplots()

for idx, risk_aversion in enumerate(risk_aversions):
    optimal_weights, max_utility, utilities, weights_list = monte_carlo_simulation(data, risk_aversion)
    
    # Plot utilities for the current risk aversion level
    ax.scatter([w[0] for w in weights_list], utilities, c=colors[idx], alpha=0.6, label=f'Risk Aversion: {risk_aversion}', s=10)
    
    # Mark the optimal weight point for the current risk aversion level with a white circle marker
    ax.scatter(optimal_weights[0], max_utility, c='w', marker='o', s=50, edgecolors=colors[idx], linewidths=1)

# Add gridlines with thin lines
ax.grid(linestyle='-', linewidth=0.5)

ax.set_xlabel('Market Asset Weight')
ax.set_ylabel('Utility')
ax.set_title('Utilities of Different Portfolio Allocations for Varying Risk Aversions')
ax.legend()
plt.show()