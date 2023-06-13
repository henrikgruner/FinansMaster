import datetime
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from datasets import get_datasets, get_shiller
import matplotlib.pyplot as plt


time_horizon = 40
start_year = 1930
end_date = start_year+40

data = get_datasets(str(start_year))
data = data[(data['Date']<np.datetime64(str(end_date)))] 


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

# The rest of the code remains unchanged
risk_aversion =10
optimal_weights, max_utility, utilities, weights_list = monte_carlo_simulation(data, risk_aversion)

# Plot utilities
plt.scatter([w[0] for w in weights_list], utilities, alpha=0.6)
plt.xlabel('Market Asset Weight')
plt.ylabel('Utility')
plt.title('Utilities of Different Portfolio Allocations')
plt.axvline(x=optimal_weights[0], color='r', linestyle='--', label=f'Optimal Market Weight: {optimal_weights[0]:.2%}')
plt.legend()
plt.show()

print("Optimal Weights:")
print("Market:", optimal_weights[0])
print("Risk-Free:", optimal_weights[1])
print("Max Utility:", max_utility)
