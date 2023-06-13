import numpy as np
from scipy.optimize import minimize

# Set the random seed for reproducibility
np.random.seed(42)

# Generate realistic data for risky asset returns for 12-month horizon
risky_mean_12_month = 0.12  # 12% mean return
risky_std_12_month = 0.20   # 20% standard deviation
risky_returns_12_month = np.random.normal(loc=risky_mean_12_month, scale=risky_std_12_month, size=100)

# Generate realistic data for risk-free asset returns for 12-month horizon
risk_free_rate_12_month = 0.20  # 20% risk-free rate
risk_free_returns_12_month = np.full(100, risk_free_rate_12_month)

# Define the utility function
def utility_function(returns, risk_aversion):
    return np.mean(returns) - 0.5 * risk_aversion * np.var(returns)

# Define the objective function
def objective_function(weights, returns_risky, returns_risk_free, risk_aversion):
    portfolio_returns = weights * returns_risky + (1 - weights) * returns_risk_free
    return -utility_function(portfolio_returns, risk_aversion)

# Define the constraint function for sum of weights
def constraint(weights):
    return np.sum(weights) - 1

# Define the initial guess for weights
initial_weights = [0.5]  # Initial weight for the risky asset

# Define the risk aversion parameter
risk_aversion = 20.0

# Define any additional constraints if needed
constraints = ({'type': 'eq', 'fun': constraint})

# Define the bounds for the weights (0% to 100%)
bounds = ((0, 1),)

# Solve the optimization problem for 12-month horizon
result_12_month = minimize(objective_function, initial_weights,
                           args=(risky_returns_12_month, risk_free_returns_12_month, risk_aversion),
                           method='SLSQP', bounds=bounds, constraints=constraints)

# Extract the optimized weight for risky asset
optimized_weight_risky = result_12_month.x[0]

print("Optimized Weights for 12-Month Horizon:")
print("Risky Asset Weight:", optimized_weight_risky)
print("Risk-Free Asset Weight:", 1 - optimized_weight_risky)
