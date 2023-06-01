import sys
sys.path.append('../')
from datasets import get_datasets, get_sp500, get_T_Bills_1M
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random
import seaborn as sns

#Reproceability
random.seed(10)

time_horizon = 40

data = get_datasets()
data['returns_with_dividends'] = data['simple_return'] + data['dividend_return']

horizons = np.arange(1, time_horizon+1)
n_portfolios = 500

cum_market_returns_distributions =np.zeros((len(horizons), n_portfolios))
cum_risk_free_returns_distributions = np.zeros((len(horizons), n_portfolios))
cum_dividends_returns_distributions = np.zeros((len(horizons), n_portfolios))

# Loop through each investment horizon
for h_idx, horizon in enumerate(horizons):
    months_in_horizon = horizon * 12
    max_start_idx = len(data) - months_in_horizon

    for i in range(n_portfolios):
        start_idx = random.randint(0, max_start_idx)
        end_idx = start_idx + months_in_horizon

        market_returns = data.loc[start_idx:end_idx, 'simple_return'].values
        risk_free_returns = data.loc[start_idx:end_idx, 'returns_rf'].values
        dividends_returns = data.loc[start_idx:end_idx, 'returns_with_dividends'].values

        cum_market_returns_portfolios = np.prod(1 + market_returns) - 1
        cum_risk_free_returns_portfolios = np.prod(1 + risk_free_returns) - 1
        cum_dividends_returns_portfolios = np.prod(1 + dividends_returns) - 1

        cum_market_returns_distributions[h_idx][i] = cum_market_returns_portfolios
        cum_risk_free_returns_distributions[h_idx][i] = cum_risk_free_returns_portfolios
        cum_dividends_returns_distributions[h_idx][i] = cum_dividends_returns_portfolios

confidence_level = 0.95

var_market = []
cvar_market = []
var_dividends = []
cvar_dividends = []

for idx, horizon in enumerate(horizons):
    var_market.append(np.percentile(100 * cum_market_returns_distributions[idx], (1 - confidence_level) * 100))
    var_dividends.append(np.percentile(100 * cum_dividends_returns_distributions[idx], (1 - confidence_level) * 100))



    var = var_market[-1]
    cvar_market.append(np.mean(100*cum_market_returns_distributions[100*cum_market_returns_distributions < var]))

    var_d = var_dividends[-1]
    cvar_dividends.append(np.mean(100*cum_dividends_returns_distributions[100*cum_dividends_returns_distributions < var_d]))



plt.figure(figsize=(10, 5))
plt.plot(horizons, var_market, label='VaR Market', marker='o')
plt.plot(horizons, cvar_market, label='cVaR Market', marker='o')
plt.plot(horizons, var_dividends, label='VaR with Dividends', marker='o')
plt.plot(horizons, cvar_dividends, label='cVaR with Dividends', marker='o')
plt.axhline(0, color='black', linestyle='--', label='Zero line')
plt.xlabel('Investment Horizon (Years)')
plt.ylabel(f'VaR ({confidence_level * 100:.0f}%)')
plt.title('VaR as a Function of Time')
plt.legend()
plt.grid()
plt.show()



