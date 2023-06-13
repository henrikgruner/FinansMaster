import datetime
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from datasets import get_datasets, get_shiller
import matplotlib.pyplot as plt
import random

time_horizon = 40

data = get_datasets()
data['returns_with_dividends'] = data['simple_return'] + data['dividend_return']

#data = data[(data['Date']<np.datetime64(str(end_date)))] 
print(data)
# Define a function to calculate the probability of market underperformance and VaR
def calculate_market_underperformance_var_cvar_terminal_wealth(market_returns, risk_free_returns, dividend_returns, initial_wealth, confidence_level=0.95):

    terminal_wealth_market = initial_wealth * np.prod(1 + market_returns)
    terminal_wealth_rf = initial_wealth * np.prod(1 + risk_free_returns)
    terminal_wealth_d = initial_wealth * np.prod(1 + dividend_returns)

    underperformance = terminal_wealth_market < terminal_wealth_rf
    underperformance_d = terminal_wealth_d < terminal_wealth_rf

    loss = terminal_wealth_market < initial_wealth
    loss_d = terminal_wealth_d < initial_wealth

    diff_returns = market_returns - risk_free_returns
    var_percentage = np.percentile(diff_returns, (1 - confidence_level) * 100)
    var_dollar = initial_wealth * abs(var_percentage)
    
    cvar_percentage = np.mean(diff_returns[diff_returns < var_percentage])
    cvar_dollar = initial_wealth * abs(cvar_percentage)
    
    return loss,loss_d, underperformance,underperformance_d, var_dollar, cvar_dollar, terminal_wealth_market, terminal_wealth_rf

# Set the random seed for reproducibility
random.seed(42)

# Number of portfolios and years
n_portfolios = 1000
n_years = 5

# Initial wealth
initial_wealth = 100

# Calculate the number of months in the specified time horizon
months_in_horizon = n_years * 12

# Calculate the maximum starting index for a random beginning
max_start_idx = len(data) - months_in_horizon

# Initialize arrays to store the underperformance results, VaR, CVaR, and terminal wealth for each portfolio
underperformance_results = np.zeros(n_portfolios, dtype=bool)
underperformance_d_results = np.zeros(n_portfolios, dtype=bool)
vars_dollar = np.zeros(n_portfolios)
cvars_dollar = np.zeros(n_portfolios)
loss_results_d = np.zeros(n_portfolios)
loss_results = np.zeros(n_portfolios)
terminal_wealth_market = np.zeros(n_portfolios)
terminal_wealth_rf = np.zeros(n_portfolios)

# Loop through each portfolio and calculate the underperformance, VaR, CVaR, and terminal wealth
for i in range(n_portfolios):
    start_idx = random.randint(0, max_start_idx)
    end_idx = start_idx + months_in_horizon

    market_returns = data.loc[start_idx:end_idx, 'returns'].values
    risk_free_returns = data.loc[start_idx:end_idx, 'returns_rf'].values
    
    dividend_returns = data.loc[start_idx:end_idx, 'returns_with_dividends'].values


    
    loss,loss_d, underperformance,underperformance_d, var_dollar, cvar_dollar, tw_market, tw_rf = calculate_market_underperformance_var_cvar_terminal_wealth(market_returns, risk_free_returns,dividend_returns, initial_wealth)
    loss_results[i] = loss
    loss_results_d[i] = loss_d
    underperformance_results[i] = underperformance
    underperformance_d_results[i] = underperformance_d

    vars_dollar[i] = var_dollar
    cvars_dollar[i] = cvar_dollar
    terminal_wealth_market[i] = tw_market
    terminal_wealth_rf[i] = tw_rf

# Calculate the probability of market underperformance, average VaR, CVaR, and terminal wealth across all simulated portfolios
prob_underperformance = np.mean(underperformance_results)
prob_underperformance_d = np.mean(underperformance_d_results)
prob_loss = np.mean(loss_results)
prob_loss_d = np.mean(loss_results_d)
avg_var_dollar = np.mean(vars_dollar)
avg_cvar_dollar = np.mean(cvars_dollar)
avg_terminal_wealth_market = np.mean(terminal_wealth_market)
avg_terminal_wealth_rf = np.mean(terminal_wealth_rf)

print(f"Investment horizon: {n_years:.4f}", f"Number of portfolios:{n_portfolios:.4f}")
print(f"Probability of Loss: {prob_loss:.4f}")
print(f"Probability of Loss with dividends: {prob_loss_d:.4f}")
print(f"Probability of Market Underperformance: {prob_underperformance:.4f}")
print(f"Probability of Market Underperformance with dividends reinvested: {prob_underperformance_d:.4f}")
print(f"Average Value at Risk (VaR) in dollars: ${avg_var_dollar:.2f}")
print(f"Average Conditional Value at Risk (CVaR): ${avg_cvar_dollar:.2f}")
print(f"Average Terminal Wealth Market Portfolio: ${avg_terminal_wealth_market:.2f}")
print(f"Average Terminal Wealth Risk-Free Portfolio: ${avg_terminal_wealth_rf:.2f}")