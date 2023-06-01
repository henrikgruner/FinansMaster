import numpy as np
import pandas as pd
import random
import time


#TODO: Sørg for å regne ut med forskjellige allokeringer med samme slices (inkl. time-diversification)
# Speedup + fair comparison. 
def calculate_utility_fixed(rm,rf,dates, market_share = 0.6):
    
    total_wealth = 100
    num_years = 25
    num_weeks = 52*(num_years-1)+1
    for week,(r_m, r_f, dato) in enumerate(zip(rm,rf,dates)):
        if(week % 52 == 0 and week != 0):
            if(week > num_weeks):
                break
        total_wealth = market_share*total_wealth*(1+r_m/100)+total_wealth*(1-market_share)*(1+r_f/100)

    #print("total return:", total_wealth/100)
    return total_wealth/100, power_function(total_wealth)


def calculate_utility(rm,rf,dates):
    total_wealth = 100
    market_share = 1
    detract_constant = 0.04
    num_years = 25
    num_weeks = 52*(num_years-1)+1
    for week,(r_m, r_f, dato) in enumerate(zip(rm,rf,dates)):
        if(week % 52 == 0 and week != 0):
            if(market_share <= 0 or week > num_weeks):
                break
            market_share = round(market_share - detract_constant,2) 
    #print("date: ",dato, "market_share:" ,market_share,"Wealth:" , total_wealth, "Utility:", total_wealth**(a)/(1-a), "R_m:", r_m, "R_f:", r_f)
        total_wealth = market_share*total_wealth*(1+(r_m+r_f)/100)+total_wealth*(1-market_share)*(1+r_f/100)

    #print("total return:", total_wealth/100)
    return total_wealth/100, power_function(total_wealth)

def power_function(wealth, a = 0.2):
    return wealth**(a)/(1-a)

def slice_df(df):
    random_idx = random.randint(0, 3722)
    df = df.iloc[random_idx:random_idx+1300+1]
    return df


def simulation(fixed = False, n = 10000, market_share = 0.6):
    utilities,returns,utilities_fixed,returns_fixed = [],[],[],[]
     
    simulations = 10000
    start = time.time()
    for _ in range(simulations):    
        df = pd.read_csv("weekly.csv", delimiter = ";")
        df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')
        df = slice_df(df)
        if(fixed):
            curr_return, curr_utility = calculate_utility_fixed(df["rm"], df["rf"],df['date'], market_share)
        else:
            curr_return, curr_utility = calculate_utility(df["rm"], df["rf"],df['date'])
        returns.append(curr_return)
        utilities.append(curr_utility)
    return np.mean(returns), np.std(returns), np.mean(utilities), np.std(utilities)


if __name__ == "__main__":
    
    for i in range(0,21):
        market_share = i/20
        returns, return_std, utility, utility_std = simulation(True, 1000, market_share)
        print("market_share", market_share, "returns",returns, "std:", return_std,"Utility", utility,"std: ", utility_std )


'''
    print("Returns", "mean: ", np.mean(returns), "std: ", np.std(returns))
    print("Utility", "mean: ", np.mean(utilities), "std: ", np.std(utilities))
    print("Returns Fixed", "mean: ", np.mean(returns_fixed), "std: ", np.std(returns_fixed))
    print("Utility Fixed", "mean: ", np.mean(utilities_fixed), "std: ", np.std(utilities_fixed))
    print((time.time()-start)/60)
    utilities,returns,utilities_fixed,returns_fixed = [],[],[],[]
     
    simulations = 10000
    start = time.time()
    for _ in range(simulations):    
        df = pd.read_csv("weekly.csv", delimiter = ";")
        df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')
        df = slice_df(df)
        curr_return, curr_utility = calculate_utility(df["rm"], df["rf"],df['date'])
        curr_return_fixed, curr_utility_fixed = calculate_utility_fixed(df["rm"], df["rf"],df['date'])
        utilities_fixed.append(curr_utility_fixed)
        returns_fixed.append(curr_return_fixed)
        returns.append(curr_return)
        utilities.append(curr_utility)

    print("Returns", "mean: ", np.mean(returns), "std: ", np.std(returns))
    print("Utility", "mean: ", np.mean(utilities), "std: ", np.std(utilities))
    print("Returns Fixed", "mean: ", np.mean(returns_fixed), "std: ", np.std(returns_fixed))
    print("Utility Fixed", "mean: ", np.mean(utilities_fixed), "std: ", np.std(utilities_fixed))
    
    print((time.time()-start)/60)
'''