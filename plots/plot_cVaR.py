import sys
sys.path.append('../')
from datasets import get_datasets, get_sp500, get_T_Bills_1M
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random
import seaborn as sns


time_horizon = 40

data = get_datasets()
data['returns_with_dividends'] = data['simple_return'] + data['dividend_return']


horizons = np.arange(5, time_horizon+1, 1)
n_portfolios = 500


cum_market_returns_distributions =np.zeros((len(horizons), n_portfolios))
cum_risk_free_returns_distributions = np.zeros((len(horizons), n_portfolios))
cum_dividends_returns_distributions = np.zeros((len(horizons), n_portfolios))
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

        cum_market_returns_portfolios = np.prod(1 + market_returns) - 1
        cum_risk_free_returns_portfolios = np.prod(1 + risk_free_returns) - 1
        cum_dividends_returns_portfolios = np.prod(1 + dividends_returns) - 1

        # Store the cumulative return distributions for the current investment horizon
        cum_market_returns_distributions[h_idx][i] = cum_market_returns_portfolios
        cum_risk_free_returns_distributions[h_idx][i] = cum_risk_free_returns_portfolios
        cum_dividends_returns_distributions[h_idx][i] = cum_dividends_returns_portfolios

    
def expected_shortfall(returns, confidence_level):
    var = np.percentile(returns, (1 - confidence_level) * 100)
    shortfall = returns[returns <= var]
    return np.mean(shortfall)

var_market_values = np.zeros(len(horizons))
var_rf_values = np.zeros(len(horizons))
var_dividends_values = np.zeros(len(horizons))

es_market_values = np.zeros(len(horizons))
es_rf_values = np.zeros(len(horizons))
es_dividends_values = np.zeros(len(horizons))

confidence_level = 0.95

for idx, horizon in enumerate(horizons):
    var_market = np.percentile(100 * cum_market_returns_distributions[idx], (1 - confidence_level) * 100)
    es_market = expected_shortfall(100 * cum_market_returns_distributions[idx], confidence_level)

    var_rf = np.percentile(100 * cum_risk_free_returns_distributions[idx], (1 - confidence_level) * 100)
    es_rf = expected_shortfall(100 * cum_risk_free_returns_distributions[idx], confidence_level)

    var_dividends = np.percentile(100 * cum_dividends_returns_distributions[idx], (1 - confidence_level) * 100)
    es_dividends = expected_shortfall(100 * cum_dividends_returns_distributions[idx], confidence_level)

    var_market_values[idx] = var_market
    es_market_values[idx] = es_market
    var_rf_values[idx] = var_rf
    es_rf_values[idx] = es_rf
    var_dividends_values[idx] = var_dividends
    es_dividends_values[idx] = es_dividends

plt.figure(figsize=(15, 5))

plt.subplot(1, 3, 1)
plt.plot(horizons, var_market_values, color='orange', linestyle='-', marker='o', label='VaR')
plt.plot(horizons, es_market_values, color='purple', linestyle='-', marker='o', label='ES')
plt.axhline(0, color='grey', linestyle='--', alpha=0.7)
plt.xlabel('Investment Horizon (years)')
plt.ylabel('Value (%)')
plt.title('Market Returns VaR and ES vs. Investment Horizon')
plt.legend()

plt.subplot(1, 3, 2)
plt.plot(horizons, var_rf_values, color='orange', linestyle='-', marker='o', label='VaR')
plt.plot(horizons, es_rf_values, color='purple', linestyle='-', marker='o', label='ES')
plt.axhline(0, color='grey', linestyle='--', alpha=0.7)
plt.xlabel('Investment Horizon (years)')
plt.ylabel('Value (%)')
plt.title('Risk-Free Returns VaR and ES vs. Investment Horizon')
plt.legend()

plt.subplot(1, 3, 3)
plt.plot(horizons, var_dividends_values, color='orange', linestyle='-', marker='o', label='VaR')
plt.plot(horizons, es_dividends_values, color='purple', linestyle='-', marker='o', label='ES')
plt.axhline(0, color='grey', linestyle='--', alpha=0.7)
plt.xlabel('Investment Horizon (years)')
plt.ylabel('Value (%)')
plt.title('Returns with Dividends VaR and ES vs. Investment Horizon')
plt.legend()

plt.tight_layout()
plt.show()

   
    
