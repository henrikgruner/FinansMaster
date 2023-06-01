import sys
sys.path.append('../')
from datasets import get_datasets, get_sp500, get_T_Bills_1M
import matplotlib.pyplot as plt
import pandas as pd

sp500 = get_sp500()
Tbills = get_T_Bills_1M()
data = sp500.merge(Tbills, on='Date')
DIVIDENDS = False
data = get_datasets()


# Create a list of different asset allocations, ranging from 0% to 100% in increments of 10%
allocations = [i/10 for i in range(0, 11)]

# Create a dictionary to store the cumulative returns for each allocation
cumulative_returns_dict = {}

# Calculate the cumulative returns for each allocation
for allocation in allocations:
    # Calculate the weighted returns for each allocation by multiplying the allocation with the S&P 500 returns and the remaining weight with the risk-free returns
    if(DIVIDENDS):
        data['returns_total'] = allocation * (data['simple_return']+data['dividend_return']) + (1 - allocation) * data['returns_rf']  # Changed 'returns_rf' to 'RF'
    else:
        data['returns_total'] = allocation * data['simple_return'] + (1 - allocation) * data['returns_rf']  # Changed 'returns_rf' to 'RF'
    # Calculate the cumulative returns for the weighted returns
    data['cumulative_returns_total'] = (1 + data['returns_total']).cumprod() - 1
    
    # Add the cumulative returns to the dictionary
    cumulative_returns_dict[allocation] = data[['Date', 'cumulative_returns_total']].rename(columns={'cumulative_returns_total': f'{allocation*100:.0f}% in S&P 500'})

# Merge the cumulative returns for each allocation into a single DataFrame
cumulative_returns_df = cumulative_returns_dict[0]
for allocation in allocations[1:]:
    cumulative_returns_df = cumulative_returns_df.merge(cumulative_returns_dict[allocation], on='Date', how='outer')

# Plot the data
fig, ax = plt.subplots(figsize=(10, 5))
for allocation in allocations:
    ax.plot(cumulative_returns_df['Date'], cumulative_returns_df[f'{allocation*100:.0f}% in S&P 500'], label=f'{allocation*100:.0f}% in S&P 500 (Dividends Reinvested)- {100-allocation*100:.0f}% in T-Bills', linewidth=2)
ax.legend(loc='upper left', fontsize=12)
ax.set_xlabel('Date', fontsize=14)
ax.set_title('Cumulative Returns with Different Allocations when Dividends are Reinvested', fontsize=16)
ax.grid(linestyle='--', linewidth=0.5)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()
plt.show()
print(cumulative_returns_df)


# Calculate the number of years in the dataset
num_years = (data['Date'].iloc[-1] - data['Date'].iloc[0]).days / 365.25

# Initialize an empty DataFrame to store allocation, annualized return, and cumulative return
latex_table_data = []

for allocation in allocations:
    cumulative_return = cumulative_returns_df[f'{allocation*100:.0f}% in S&P 500'].iloc[-1] * 100
    annualized_return = ((1 + cumulative_return / 100) ** (1 / num_years) - 1) * 100
    
    latex_table_data.append({
        "Allocation": f"{allocation*100:.0f}% in S&P 500",
        "Annualized Return": annualized_return,
        "Cumulative Return": cumulative_return
    })

# Create the DataFrame
latex_table_df = pd.DataFrame(latex_table_data)

# Set the index to the 'Allocation' column
latex_table_df.set_index("Allocation", inplace=True)

# Custom float format for displaying percentages
def percentage_formatter(x):
    return f"{x:.2f}%"

# Convert the DataFrame to a LaTeX table
latex_table = latex_table_df.to_latex(float_format=percentage_formatter)

print(latex_table)







