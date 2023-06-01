import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
sys.path.append('../')
from datasets import get_datasets, get_shiller

import numpy as np
import pandas as pd
from scipy.optimize import minimize
from datasets import get_datasets, get_shiller
import matplotlib.pyplot as plt
import random
import seaborn as sns

#Reproceability
random.seed(10)
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

    
    diff_returns = np.cumsum(market_returns - risk_free_returns)
    var_percentage = np.percentile(diff_returns, (1 - confidence_level) * 100)
    
    cvar_percentage = np.mean(diff_returns[diff_returns < var_percentage])
    
    return loss,loss_d, underperformance,underperformance_d, var_percentage, cvar_percentage, terminal_wealth_market, terminal_wealth_rf, terminal_wealth_d
# Define the range of investment horizons in years
horizons = np.arange(1, time_horizon+1)

n_portfolios = 500

# Initialize an array to store the probability of market underperformance for each investment horizon
prob_underperformance_horizons = np.zeros(len(horizons))
prob_loss_horizons = np.zeros(len(horizons))

prob_underperformance_horizons_d = np.zeros(len(horizons))
prob_loss_horizons_d = np.zeros(len(horizons))


underperformance_results = np.zeros(n_portfolios, dtype=bool)
underperformance_d_results = np.zeros(n_portfolios, dtype=bool)
var = np.zeros(n_portfolios)
cvar = np.zeros(n_portfolios)
loss_results_d = np.zeros(n_portfolios)
loss_results = np.zeros(n_portfolios)
terminal_wealth_market = np.zeros(n_portfolios)
terminal_wealth_rf = np.zeros(n_portfolios)
terminal_wealth_d = np.zeros(n_portfolios)



avg_var = np.zeros(len(horizons))
avg_cvar = np.zeros(len(horizons))
avg_terminal_wealth_market = np.zeros(len(horizons))
avg_terminal_wealth_rf = np.zeros(len(horizons))
avg_terminal_wealth_d = np.zeros(len(horizons))

# Loop through each investment horizon
for h_idx, horizon in enumerate(horizons):
    # Calculate the number of months in the specified time horizon
    months_in_horizon = horizon * 12
    max_start_idx = len(data) - months_in_horizon

    # Initial wealth
    initial_wealth = 100


    # Loop through each portfolio and calculate the underperformance, VaR, CVaR, and terminal wealth
    for i in range(n_portfolios):
        start_idx = random.randint(0, max_start_idx)
        end_idx = start_idx + months_in_horizon

        market_returns = data.loc[start_idx:end_idx, 'simple_return'].values
        risk_free_returns = data.loc[start_idx:end_idx, 'returns_rf'].values
        dividends_returns = data.loc[start_idx:end_idx, 'returns_with_dividends'].values
        loss,loss_d, underperformance,underperformance_d, var_percentage, cvar_percentage, tw_market, tw_rf, tw_d = calculate_market_underperformance_var_cvar_terminal_wealth(market_returns, risk_free_returns, dividends_returns, initial_wealth)

        loss_results[i] = loss
        loss_results_d[i] = loss_d
        underperformance_results[i] = underperformance
        underperformance_d_results[i] = underperformance_d

        var[i] = var_percentage
        cvar[i] = cvar_percentage
        terminal_wealth_market[i] = tw_market
        terminal_wealth_rf[i] = tw_rf
        terminal_wealth_d[i] = tw_d

    # Calculate the probability of market underperformance for the current investment horizon
    prob_underperformance_horizons[h_idx] = np.mean(underperformance_results)
    prob_underperformance_horizons_d[h_idx] = np.mean(underperformance_d_results)
    prob_loss_horizons[h_idx] = np.mean(loss_results)
    prob_loss_horizons_d[h_idx] = np.mean(loss_results_d)
    avg_var[h_idx] = np.mean(var)
    avg_cvar[h_idx] = np.mean(cvar)
    avg_terminal_wealth_market[h_idx] = np.mean(terminal_wealth_market)
    avg_terminal_wealth_rf[h_idx] = np.mean(terminal_wealth_rf)
    avg_terminal_wealth_d[h_idx] = np.mean(terminal_wealth_d)




# Create a graph of the probability of underperformance over different investment horizons
plt.figure(figsize=(10, 6))
plt.plot(horizons, prob_underperformance_horizons, marker='o', linestyle='-', linewidth=2, markersize=6, label = "Without dividends reinvested")
plt.plot(horizons, prob_underperformance_horizons_d, marker='o', linestyle='-', linewidth=2, markersize=6, label = "Dividends reinvested")
plt.xlabel("Investment Horizon (Years)", fontsize=14)
plt.ylabel("Probability of Market Underperformance", fontsize=14)
plt.title("Probability of Market Underperformance over Different Investment Horizons", fontsize=16)
plt.legend()
plt.grid(True)
plt.show()



plt.figure(figsize=(10, 6))
plt.plot(horizons, prob_loss_horizons, marker='o', linestyle='-', linewidth=2, markersize=6, label = "Without dividends reinvested")
plt.plot(horizons, prob_loss_horizons_d, marker='o', linestyle='-', linewidth=2, markersize=6, label = "Dividends reinvested")
plt.xlabel("Investment Horizon (Years)", fontsize=14)
plt.ylabel("Probability of loss", fontsize=14)
plt.title("Probability of loss over Different Investment Horizons", fontsize=16)
plt.legend()
plt.grid(True)
plt.show()


plt.figure(figsize=(10, 6))
plt.plot(horizons, avg_var, marker='o', linestyle='-', linewidth=2, markersize=6, label = "Value at Risk")
plt.plot(horizons, avg_cvar, marker='o', linestyle='-', linewidth=2, markersize=6, label = "Conditional Value at Risk")
plt.xlabel("Investment Horizon (Years)", fontsize=14)
plt.ylabel("Average Value-at-Risk (VaR)", fontsize=14)
plt.title("Average VaR and cVaR over Different Investment Horizons", fontsize=16)
plt.grid(True)
plt.show()


plt.figure(figsize=(10, 6))
plt.plot(horizons, avg_terminal_wealth_d, marker='o', linestyle='-', linewidth=2, markersize=6, label = "Average market return with dividends reinvested")
plt.plot(horizons, avg_terminal_wealth_market, marker='o', linestyle='-', linewidth=2, markersize=6, label = "Average market return")
plt.plot(horizons, avg_terminal_wealth_rf, marker='o', linestyle='-', linewidth=2, markersize=6, label = "Average T-Bill 1M return")
plt.xlabel("Investment Horizon (Years)", fontsize=14)
plt.ylabel("Average Terminal Wealth in Market Portfolio (%)", fontsize=14)
plt.title("Average Terminal Wealth in Market Portfolio over Different Investment Horizons", fontsize=16)
plt.legend()
plt.grid(True)
plt.show()



