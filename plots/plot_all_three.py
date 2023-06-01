import sys
sys.path.append('../')
from datasets import get_datasets
import matplotlib.pyplot as plt

merged_data = get_datasets()

merged_data.set_index('Date', inplace=True)
# Plot the data
fig, ax = plt.subplots(figsize=(12, 8))
ax.plot(merged_data['cumulative_returns'], label='Cumulative S&P 500 Returns', linewidth=2, color='blue')
ax.plot(merged_data['cum_return_with_dividends'], label='Cumulative S&P 500 Returns with Dividends Reinvested', linewidth=2, color='orange')
ax.plot(merged_data['cumulative_rf'], label='Cumulative T-bills 1 Month Returns', linewidth=2, color='green')

ax.legend(loc='upper left', fontsize=12)
ax.set_xlabel('Date', fontsize=14)
ax.set_ylabel('Cumulative Returns', fontsize=14)
ax.set_title(f'Cumulative S&P 500 Returns vs. Cumulative T-bills 1 Month Returns - Final year: {2023}', fontsize=16)
ax.grid(linestyle='--', linewidth=0.5)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
last_cumulative_return = merged_data['cumulative_returns'].iloc[-1]
last_cumulative_rf = merged_data['cumulative_rf'].iloc[-1]
last_cumulative_return_with_dividends = merged_data['cum_return_with_dividends'].iloc[-1]
last_date = merged_data.index[-1]

# Add annotations for the final point of both curves
bbox_props = dict(boxstyle='round', facecolor='white', edgecolor='gray', alpha=0.8)
ax.annotate(f"{last_cumulative_return:.2%}", xy=(last_date, last_cumulative_return), xytext=(10, 10), textcoords='offset points', fontsize=12, bbox=bbox_props)
ax.annotate(f"{last_cumulative_rf:.2%}", xy=(last_date, last_cumulative_rf), xytext=(10, 0), textcoords='offset points', fontsize=12, bbox=bbox_props)
ax.annotate(f"{last_cumulative_return_with_dividends:.2%}", xy=(last_date, last_cumulative_return_with_dividends), xytext=(10, 10), textcoords='offset points', fontsize=12, bbox=bbox_props)

plt.tight_layout()
plt.show()