Changes after 1th of June are only rearranging folders/files and adding README, no code changes.

As Github will not render my jupyter files, one could paste the github-link to each jypter notebook to "https://nbviewer.org/", and receive the results without cloning the repo.

# FinansMaster
Datasets.py fetches the data from S&P500 and Robert shiller [1]. To run the analyses, clone the repository and run the notebook files (.ipynb). The code for all plots for the theory part of the thesis is located in plots or old.

## Descriptive.ipynb
Returns descriptive statistics of all the portfolios

## Options.ipynb
Calculates the shortfall insurance risk with market data

## Portfolio_stats.ipynb
Calculates the expected risk metrics of the portfolio including volatility, returns, VaR, cVaR, shortfall probability etc

## Utility_stream.ipynb and Utility_months.ipynb
Uses the expected utility stream to calculate the optimal allocation to risky assets. 

# Sources
[1] Robert J Shiller. Irrational exuberance. In Irrational exuberance. Princeton university
press, 2015.
