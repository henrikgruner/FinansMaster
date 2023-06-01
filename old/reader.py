import numpy as np
import matplotlib.pyplot as plt


def plotter(x,y, title,y_label):
    plt.plot(x,y)
    plt.title(title)
    plt.xticks([x for x in range(0,101) if x % 5 == 0])
    plt.xlabel("Proportion of portfolio in risk-free asset")
    plt.ylabel("Expected"+y_label)

    plt.grid()
    plt.show()



market_share, returns, returns_std, utility, utility_std = [],[],[],[],[]

with open("test.txt") as file:
    for line in file:
        line = line.rstrip()
        lines = line.split(" ")
        for i,l in enumerate(lines):
            if(i % 2 != 0):
                print(l,i)
                try:
                    if(i == 9):
                        lines[10] = eval(lines[10])
                    else:    
                        lines[i] = eval(l)
                except:
                    pass
                    
            
        market_share.append(lines[1]*100)
        returns.append(lines[3]*100)
        returns_std.append(lines[5])
        utility.append(lines[7])
        utility_std.append(lines[10])


print(market_share, returns, returns_std, utility, utility_std)
plotter(market_share,returns, "Total return over a 25 year time horizon with fixed allocations during the entire period","total return")
plotter(market_share,returns_std,"Standard deviation over a 25 year time horizon with fixed allocations during the entire period", "standard deviaton")
plotter(market_share,utility, "End utility over a 25 year time horizon with fixed allocations during the entire period", "utility")
