import sys
sys.path.append('../')
from datasets import get_datasets, get_sp500, get_T_Bills_1M
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random
import seaborn as sns

#Reproceability
random.seed(0)

time_horizon = 40

data = get_datasets()
data['returns_with_dividends'] = data['simple_return'] + data['dividend_return']

def expected_shortfall(returns, confidence_level):
    var = np.percentile(returns, (1 - confidence_level) * 100)
    shortfall = returns[returns <= var]
    return np.mean(shortfall)

horizons = np.arange(1, time_horizon+1, 1)
n_portfolios = 1000


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

    

confidence_level = 0.95

for idx, horizon in enumerate(horizons):
    plt.figure(figsize=(15, 5))

     #plt.subplot(1, 3, 2)
#    sns.histplot(100 * cum_risk_free_returns_distributions[idx], bins=50, kde=True, alpha=0.75)
#    plt.axvline(100 * np.mean(cum_risk_free_returns_distributions[idx]), color='red', linestyle='--', label='Mean')
#    var_rf = np.percentile(100 * cum_risk_free_returns_distributions[idx], (1 - confidence_level) * 100)
#    es_rf = expected_shortfall(100 * cum_risk_free_returns_distributions[idx], confidence_level)
#    plt.axvline(es_rf, color='purple', linestyle='--', label=f'cVaR ({confidence_level * 100:.0f}%)')
#    plt.axvline(var_rf, color='orange', linestyle='--', label=f'VaR ({confidence_level * 100:.0f}%)')
#    plt.xlabel('Cumulative Risk-Free Returns (%)')
#    plt.ylabel('Frequency')
#    plt.title(f'Cumulative Risk-Free Returns Distribution\nfor {horizon} Year(s) Investment Horizon')
#    plt.legend()

    plt.subplot(1, 2, 1)
    sns.histplot(100 * cum_market_returns_distributions[idx], bins=50, kde=True, alpha=0.75)
    plt.axvline(100 * np.mean(cum_market_returns_distributions[idx]), color='red', linestyle='--', label='Mean')
    var_market = np.percentile(100 * cum_market_returns_distributions[idx], (1 - confidence_level) * 100)
    plt.axvline(var_market, color='orange', linestyle='--', label=f'VaR ({confidence_level * 100:.0f}%)')
    es_market = expected_shortfall(100 * cum_market_returns_distributions[idx], confidence_level)
    plt.axvline(es_market, color='purple', linestyle='--', label=f'cVaR ({confidence_level * 100:.0f}%)')
    plt.xlabel('Cumulative Market Returns (%)')
    plt.ylabel('Frequency')
    plt.title(f'Cumulative Market Returns Distribution\nfor {horizon} Year(s) Investment Horizon')
    plt.legend()

    plt.subplot(1, 2, 2)
    sns.histplot(100 * cum_dividends_returns_distributions[idx], bins=50, kde=True, alpha=0.75)
    plt.axvline(100 * np.mean(cum_dividends_returns_distributions[idx]), color='red', linestyle='--', label='Mean')
    var_dividends = np.percentile(100 * cum_dividends_returns_distributions[idx], (1 - confidence_level) * 100)
    plt.axvline(var_dividends, color='orange', linestyle='--', label=f'VaR ({confidence_level * 100:.0f}%)')
    es_dividends = expected_shortfall(100 * cum_dividends_returns_distributions[idx], confidence_level)
    plt.axvline(es_dividends, color='purple', linestyle='--', label=f'cVaR ({confidence_level * 100:.0f}%)')
    plt.xlabel('Cumulative Returns with Dividends (%)')
    plt.ylabel('Frequency')
    plt.title(f'Cumulative Returns with Dividends Distribution\nfor {horizon} Year(s) Investment Horizon')
    plt.legend()

    plt.tight_layout()
    plt.savefig('imgs/'+str(horizon) + '_year.png', bbox_inches='tight')
    plt.close()



    
