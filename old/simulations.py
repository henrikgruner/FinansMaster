import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datasets import get_datasets, get_shiller


dataset = get_datasets()

def crra_utility(wealth, risk_aversion_coeff):
    if risk_aversion_coeff == 1:
        return np.log(wealth)
    else:
        return (wealth ** (1 - risk_aversion_coeff)) / (1 - risk_aversion_coeff)

def cara_utility(wealth, risk_aversion_coeff):
    return 1 - np.exp(-risk_aversion_coeff * wealth) / risk_aversion_coeff


def periodic_and_total_crra_utility(dataset, risk_aversion_coeff, returns_col='returns', wealth_col='cum_returns'):
    periodic_utilities = [crra_utility(1 + returns, risk_aversion_coeff) for returns in dataset[returns_col]]
    total_periodic_utility = sum(periodic_utilities)
    
    end_wealth = dataset[wealth_col].iloc[-1]
    total_utility = crra_utility(end_wealth, risk_aversion_coeff)
    
    return total_periodic_utility, total_utility

def periodic_and_total_cara_utility(dataset, risk_aversion_coeff, returns_col='returns', wealth_col='cum_returns'):
    periodic_utilities = [cara_utility(1 + returns, risk_aversion_coeff) for returns in dataset[returns_col]]
    total_periodic_utility = sum(periodic_utilities)
    
    end_wealth = dataset[wealth_col].iloc[-1]
    total_utility = cara_utility(end_wealth, risk_aversion_coeff)
    
    return total_periodic_utility, total_utility


periodic_crra_market, total_crra_market = periodic_and_total_crra_utility(dataset, 3, returns_col='returns', wealth_col='cum_return')
periodic_crra_rf, total_crra_rf = periodic_and_total_crra_utility(dataset, 3, returns_col='returns_rf', wealth_col='cumulative_rf')

periodic_cara_market, total_cara_market = periodic_and_total_cara_utility(dataset, 3, returns_col='returns', wealth_col='cum_return')
periodic_cara_rf, total_cara_rf = periodic_and_total_cara_utility(dataset, 3, returns_col='returns_rf', wealth_col='cumulative_rf')


print("RF-", "CRRA:", periodic_crra_rf, total_crra_rf, "CARA",periodic_cara_rf, total_cara_rf)
print("Market-", "CRRA:", periodic_crra_market, total_crra_market, "CARA",periodic_cara_market, total_cara_market)
