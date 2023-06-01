import datetime
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from datasets import get_datasets, get_shiller
import matplotlib.pyplot as plt


data = get_datasets()



def utility_function(weights, returns_market, returns_rf, volatility_market, risk_aversion):
    portfolio_return = weights[0] * returns_market + weights[1] * returns_rf
    portfolio_volatility = weights[0] * volatility_market
    portfolio_variance = portfolio_volatility**2
    utility = np.mean(portfolio_return) - risk_aversion * np.mean(portfolio_variance)
    return -utility

# The previous code remains unchanged until the monte_carlo_simulation function

def monte_carlo_simulation(data, risk_aversion, num_simulations=1000, time_horizon=40):
    np.random.seed(42)
    optimal_weights = None
    max_utility = float('-inf')
    
    # Get the total number of years in the data
    total_years = len(data['returns']) // 12
    
    # Calculate the number of overlapping 40-year periods
    num_periods = total_years - time_horizon + 1
    
    # Initialize an array to store the optimal weights for each period
    optimal_weights_all_periods = np.zeros((num_periods, 2))
    
    for period in range(num_periods):
        # Select a 40-year subset of the data for the current period
        start_year = period
        end_year = start_year + time_horizon
        data_subset = {
            'returns': data['returns'][start_year:end_year],
            'returns_rf': data['returns_rf'][start_year:end_year],
            'volatility_market': data['volatility_market'][start_year:end_year]
        }
        
        max_utility_period = float('-inf')
        optimal_weights_period = None
        
        for i in range(num_simulations):
            weights = np.random.dirichlet(np.ones(2), size=1).flatten()
            utility = -utility_function(weights, data_subset['returns'], data_subset['returns_rf'], data_subset['volatility_market'], risk_aversion)
            
            if utility > max_utility_period:
                max_utility_period = utility
                optimal_weights_period = weights
                
        optimal_weights_all_periods[period] = optimal_weights_period
    
    # Calculate the average optimal weights across all periods
    optimal_weights = np.mean(optimal_weights_all_periods, axis=0)
    
    return optimal_weights, optimal_weights_all_periods


risk_aversion = 1
optimal_weights, optimal_weights_all_periods = monte_carlo_simulation(data, risk_aversion)

print("Optimal Weights:")
print("Market:", optimal_weights[0])
print("Risk-Free:", optimal_weights[1])

# Create a plot showing how the allocation changes from the investment start
start_year = 1928
investment_start_years = np.arange(start_year, start_year + len(optimal_weights_all_periods), 1)
market_weights = [weights[0] for weights in optimal_weights_all_periods]

plt.plot(investment_start_years, market_weights, label="Market")

plt.xlabel("Investment Start Year")
plt.ylabel("Optimal Market Allocation")
plt.title("Optimal Market Allocation Changes from Investment Start")

tick_positions = investment_start_years[::5]
tick_labels = np.arange(start_year, start_year + len(investment_start_years), 5)
plt.xticks(tick_positions[:len(tick_labels)], tick_labels, rotation=45)

plt.legend()
plt.grid()
plt.show()