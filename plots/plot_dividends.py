import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
sys.path.append('../')
from datasets import get_datasets, get_shiller


shiller_data = get_shiller()

# Drop the rows where all values are missing


# Reset the index
shiller_data.reset_index(drop=True, inplace=True)

# Convert the float values in the 'Date' column to strings
shiller_data['Date'] = shiller_data['Date'].apply(lambda x: '{:.2f}'.format(x))

# Calculate simple returns for price and dividends
shiller_data['simple_return'] = shiller_data['P'].pct_change()
shiller_data['dividend_return'] = ((shiller_data['D']/12) / shiller_data['P']).shift(1)

# Calculate cumulative returns for price
shiller_data['cum_return'] = (1 + shiller_data['simple_return']).cumprod()

# Calculate cumulative returns with dividends reinvested
shiller_data['cum_return_with_dividends'] = (1 + shiller_data['simple_return'] + shiller_data['dividend_return']).cumprod()

# Plot the cumulative returns
sns.set(style='whitegrid')
plt.figure(figsize=(12, 8))
plt.plot(shiller_data['cum_return'], label='Cumulative Return')
plt.plot(shiller_data['cum_return_with_dividends'], label='Cumulative Return with Dividends')

# Add title, labels, and legend
plt.title('Cumulative Returns with and without Dividends', fontsize=16)
plt.xlabel('Time', fontsize=14)
plt.ylabel('Cumulative Return', fontsize=14)
plt.legend(fontsize=12)

# Save the plot to a file
plt.savefig('cumulative_returns_plot.png', dpi=300)

# Display the plot
plt.show()

# Display the first few rows
print(shiller_data)
