import numpy as np
import pandas as pd

#rf = 0.04
#rm = 0.12
#stdrm = 0.16
#initial_wealth = 1000

rf = 0.05
rm = 0.12
stdrm = 0.20
initial_wealth = 1000000
unit = 10**6
np.random.seed(0)
risk_free_ports = []
risky_ports = []
tenth_percentiles = []
ninety_percentiles = []
probability_underperform = []
underperforming_means = []
time_periods = [1,5,10,20,30,40,50]

for time in time_periods:
    rf_free_wealth = initial_wealth*np.exp(rf*time)
    risk_free_ports.append(rf_free_wealth/unit)
    mean = []
    n = 100000
    for _ in range(n):
        mean.append(initial_wealth*np.exp(rm*time+stdrm*np.sqrt(time)*np.random.standard_normal()))

    tenth_percentiles.append(np.percentile(mean,10)/unit)

    ninety_percentiles.append(np.percentile(mean,90)/unit)

  
    underperforming_values = np.extract(np.array(mean) < rf_free_wealth, np.array(mean))
    underperforming_mean = np.mean(underperforming_values)

    underperforming_means.append(underperforming_mean/unit)

    probability_of_underperforming = np.size(underperforming_values)/n

    probability_underperform.append(probability_of_underperforming*100)

    risky_ports.append(np.mean(mean)/unit)


df = pd.DataFrame(
    {'periods': time_periods,
    'risk_free_ports': risk_free_ports,
     'risky_ports': risky_ports,
     'tenth_percentiles': tenth_percentiles,
     'ninety_percentiles': ninety_percentiles,
     'probability_underperform': probability_underperform,
     'underperforming_means': underperforming_means
    })

with open("my_table.tex", "w") as f:
    f.write("\\begin{tabular}{" + " | ".join(["c"] * len(df.columns)) + "}\n")
    for i, row in df.iterrows():
        f.write(" & ".join([str(round(x,1)) for x in row.values]) + " \\\\\n")
    f.write("\\end{tabular}")

print(df.to_latex())