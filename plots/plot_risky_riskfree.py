import sys
sys.path.append('../')
from datasets import get_datasets, get_sp500, get_T_Bills_1M
import matplotlib.pyplot as plt
import pandas as pd

sp500 = get_sp500()
Tbills = get_T_Bills_1M()
data = sp500.merge(Tbills, on='Date')

#print(data)
import matplotlib.pyplot as plt


def plot_cumulative_returns(df, returns_col='returns', rf_col='RF', figsize=(10,5)):
    """
    Plot cumulative returns and cumulative risk-free returns over time.

    Args:
        df (pd.DataFrame): A pandas DataFrame containing 'Date', 'returns', and 'RF' columns.
        returns_col (str): The name of the column containing returns data. Default is 'returns'.
        rf_col (str): The name of the column containing risk-free rate data. Default is 'RF'.
        figsize (tuple): The size of the figure in inches. Default is (10, 5).

    Returns:
        None
    """
    # Validate input DataFrame
    required_cols = ['Date', returns_col, rf_col]
    if not all(col in df.columns for col in required_cols):
        raise ValueError(f"DataFrame must contain the following columns: {required_cols}")
    df = df.copy()  # avoid modifying the original DataFrame
    
    # Convert Date column to datetime type and set it as index
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    
    # Calculate total cumulative returns in the final year
    final_year = df.index.year[-1]
    total_return = (1 + df.loc[df.index.year == final_year, returns_col]).cumprod().iloc[-1] - 1
    
    # Create cumulative returns and cumulative risk-free returns columns
    df['cumulative_returns'] = (1 + df[returns_col]).cumprod() - 1
    df['cumulative_rf'] = (1 + df[rf_col]).cumprod() - 1
    last_date = df.index[-1]
    last_cumulative_return = df['cumulative_returns'].iloc[-1]
    last_cumulative_rf = df['cumulative_rf'].iloc[-1]
    
    # Plot the data
    fig, ax = plt.subplots(figsize=figsize)

    
    ax.plot(df['cumulative_returns'], label='Cumulative S&P 500 Returns', linewidth=2, color='blue')
    ax.plot(df['cumulative_rf'], label='Cumulative T-bills 1 Month Returns', linewidth=2, color='green')
    ax.legend(loc='upper left', fontsize=12)
    ax.set_xlabel('Date', fontsize=14)
    ax.set_ylabel('Cumulative Returns', fontsize=14)
    ax.set_title(f'Cumulative S&P 500 Returns vs. Cumulative T-bills 1 Month Returns - Final year: {final_year}', fontsize=16)
    ax.grid(linestyle='--', linewidth=0.5)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    
    # Add annotations for the final point of both curves
    bbox_props = dict(boxstyle='round', facecolor='white', edgecolor='gray', alpha=0.8)
    ax.annotate(f"{last_cumulative_return:.2%}", xy=(last_date, last_cumulative_return), xytext=(10, 10), textcoords='offset points', fontsize=12, bbox=bbox_props)
    ax.annotate(f"{last_cumulative_rf:.2%}", xy=(last_date, last_cumulative_rf), xytext=(10, -20), textcoords='offset points', fontsize=12, bbox=bbox_props)
    
    plt.tight_layout()
    plt.show()


plot_cumulative_returns(data.dropna())