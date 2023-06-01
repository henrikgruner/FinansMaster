import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime

# Set the parameters for the Ornstein-Uhlenbeck process
mu = 0.12      # Long-term mean
theta = 0.15   # Speed of reversion
sigma = 0.2    # Volatility
dt = 1         # Time step in days
T = 1000       # Total time in days
n = int(T/dt)  # Number of time steps
np.random.seed(0)

# Initialize the process
R = np.zeros(n)
R[0] = np.random.normal(mu, sigma)
R_w = np.zeros(n)
R_w[0] = mu


# Generate the mean-reverting process
for t in range(1, n):
    dW = np.random.normal(0, np.sqrt(dt))  # Wiener process
    dR = theta * (mu - R[t-1]) * dt + sigma * dW
    R[t] = R[t-1] + dR
    epsilon = np.random.normal(0, sigma)  # Random variable from a normal distribution
    R_w[t] = R_w[t-1] + epsilon

# Generate a list of dates for the x-axis
start_date = datetime.date(2023, 1, 1)
dates = [start_date + datetime.timedelta(days=i) for i in range(n)]


# Plot the process
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(dates, R, label='Mean Reversion process')
ax.plot(dates, R_w, label='Random Walk Process')

ax.axhline(mu, color='red', linestyle='--', label='Long-term mean')
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))  # Set major ticks every 3 months
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))  # Format the date as 'Month Year'
plt.xticks(rotation=45)
plt.legend()
plt.title('Simulation of a Mean-Reverting Time Series and Random Walk Over Time')
plt.xlabel('Date')
plt.ylabel('Return')
plt.tight_layout()
plt.show()



