def calculate_annualized_returns(cumulative_returns, horizon):
    annualized_return = ((cumulative_returns + 1) ** (1 / horizon)) - 1
    return annualized_return

# Example usage
cumulative_returns = -0.21  # Replace with your own data
horizon = 1  # Replace with the number of years

ann_returns = calculate_annualized_returns(cumulative_returns, horizon)
print(f"Annualized Returns: {ann_returns:.2%}")
