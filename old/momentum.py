import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime

# Set the parameters for the random walk
mu = 0.12      # Mean return
sigma = 0.2    # Standard deviation
dt = 1         # Time step in days
T = 1000       # Total time in days
n = int(T/dt)  # Number of time steps
lookback = 10  # Lookback period for momentum calculation
np.random.seed(0)

# Initialize the process
R = np.zeros(n)
R[0] = mu

# Generate the random walk process
for t in range(1, n):
    epsilon = np.random.normal(0, sigma)  # Random variable from a normal distribution
    R[t] = R[t-1] + epsilon

# Calculate momentum
M = np.zeros(n)
for t in range(lookback, n):
    M[t] = R[t] - R[t-lookback]

# Generate a list of dates for the x-axis
start_date = datetime.date(2023, 1, 1)
dates = [start_date + datetime.timedelta(days=i) for i in range(n)]

# Plot the returns and momentum
fig, (ax1, ax2) = plt.subplots(2, figsize=(10, 10))
ax1.plot(dates, R, label='Return')
ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=3))  # Set major ticks every 3 months
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))  # Format the date as 'Month Year'
ax1.set_ylabel('Return')
ax1.legend()

ax2.plot(dates, M, label='Momentum', color='orange')
ax2.axhline(0, color='red', linestyle='--', label='Zero momentum')
ax2.xaxis.set_major_locator(mdates.MonthLocator(interval=3))  # Set major ticks every 3 months
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))  # Format the date as 'Month Year'
plt.xticks(rotation=45)
ax2.set_xlabel('Date')
ax2.set_ylabel('Momentum')
ax2.legend()

plt.tight_layout()
plt.show()
