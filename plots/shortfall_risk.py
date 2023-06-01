import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

# asset parameters
expected_return = 0.12
volatility = 0.20

# risk-free rate
risk_free_rate = 0.05

# standardize the risk-free rate
z = (risk_free_rate - expected_return) / volatility

# compute the probability of underperformance
prob_underperformance = stats.norm.cdf(z)

# Define the distribution
dist = stats.norm(loc=expected_return, scale=volatility)

# Generate values
values = np.linspace(expected_return - 3*volatility, expected_return + 3*volatility, 100)

# Generate pdf values
pdf_values = dist.pdf(values)

# Create the plot
plt.figure(figsize=(10,6))
plt.plot(values, pdf_values, lw=2)

# Customize the title and labels
plt.title('Distribution of Returns and Underperformance', fontsize=14)
plt.xlabel('Returns', fontsize=12)
plt.ylabel('Probability Density', fontsize=12)

# Customize the grid and spines
plt.grid(alpha=0.5)
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)

# Shade the underperformance region
underperformance_values = np.linspace(expected_return - 3*volatility, risk_free_rate, 100)
underperformance_pdf = dist.pdf(underperformance_values)
plt.fill_between(underperformance_values, underperformance_pdf, color='red', alpha=0.3)

# Annotate the risk-free rate
plt.axvline(x=risk_free_rate, color='red', linestyle='--', lw=1.5)
plt.annotate(f'Risk-free rate: {risk_free_rate*100:.1f}%', (risk_free_rate, max(pdf_values)/2), 
             textcoords="offset points", xytext=(-15,10), ha='center', fontsize=9, color='red', 
             bbox=dict(facecolor='white', edgecolor='red', boxstyle='round,pad=0.2'))

# Annotate the probability of underperformance
plt.text(expected_return - 3*volatility, max(pdf_values)*0.9, f'Prob. of Underperformance: {prob_underperformance*100:.2f}%', fontsize=10, bbox=dict(facecolor='white', alpha=0.8))

# Annotate asset parameters
plt.text(expected_return - 3*volatility, max(pdf_values)*0.8, f'Expected Return: {expected_return*100:.2f}%\nVolatility: {volatility*100:.2f}%', fontsize=10, bbox=dict(facecolor='white', alpha=0.8))

plt.show()
