import pandas as pd
import zipfile
import urllib.request
from pandas_datareader import data as pdr
import yfinance as yfin
import numpy as np


yfin.pdr_override()

def get_sp500(date = ''):
    sp500 = pdr.get_data_yahoo("^GSPC", start='1900-01-01')
    sp500.reset_index(inplace=True)
        
    sp500['Date'] = sp500['Date'].dt.date
    if(date != ''):
        sp500 = sp500[(sp500['Date']>np.datetime64(date))] 
    sp500['returns'] = sp500['Adj Close'].pct_change()
    sp500['cumulative_returns'] = (1 + sp500['returns']).cumprod() - 1
    return sp500

def get_T_Bills_1M(date = ''):
    url = "http://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_Factors_daily_CSV.zip"
    filename = "fama_dai.zip"
    urllib.request.urlretrieve(url, filename)

    with zipfile.ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall()


    rf = pd.read_csv("F-F_Research_Data_Factors_daily.csv", skiprows=3,skipfooter=2, engine='python')
    rf = rf.rename(columns={rf.columns[0]: "Date"})
    rf["Date"] = pd.to_datetime(rf["Date"], format='%Y%m%d').dt.date
    if(date != ''):
        rf = rf[(rf['Date']>np.datetime64(date))]     
    rf['RF'] = rf['RF']/100
    rf['cumulative_rf'] = (1 + rf['RF']).cumprod() - 1
    return rf


def merge_datasets(sp500, tbills):
    data = sp500.merge(tbills, on='Date')
    data['returns_rf'] = data['RF']
    data = data[['Date', 'returns', 'returns_rf','cumulative_returns','cumulative_rf']].dropna()
    return data

def get_shiller():
    # Load the shiller_data dataframe
    url = 'http://www.econ.yale.edu/~shiller/data/ie_data.xls'
    shiller_data = pd.read_excel(url, sheet_name='Data', header=7, engine='xlrd')[:-1]

    # Drop the unnecessary columns
    shiller_data.fillna(0, inplace=True)
    shiller_data.drop(columns=['Price', 'Dividend', 'Yield', 'Returns', 'Returns.1', 'Returns.2', 'TR CAPE', 'CAPE', 'Earnings', 'Earnings.1', 'Rate GS10', 'E', 'CPI', 'Unnamed: 15', 'Unnamed: 13', 'Price.1', 'Real Return', 'Real Return.1', 'Fraction'], inplace=True)

    # Calculate simple returns for price and dividends

    shiller_data['Date'] = shiller_data['Date'].apply(lambda x: '{:.2f}'.format(x))
    shiller_data['Date'] = pd.to_datetime(shiller_data['Date'], format='%Y.%m')
    return shiller_data


def get_monthly_returns(df, return_col):
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    df_monthly = df[return_col].add(1).resample('M').apply(lambda x: x.cumprod()[-1] - 1)
    df_monthly = df_monthly.reset_index()
    df_monthly['cumulative_'+return_col.lower()] = (df_monthly[return_col]+1).cumprod()
    return df_monthly.reset_index()

def get_datasets(date = ''):

# Get the sp500 and Tbills data
    sp500 = get_sp500(date)
    tbills = get_T_Bills_1M(date)
    shiller_data = get_shiller()

    sp500_monthly = get_monthly_returns(sp500, 'returns')
    tbills_monthly = get_monthly_returns(tbills, 'RF')
    #print(sp500)
    #print(tbills)
    #print(sp500_monthly)
    #print(tbills_monthly)
    # Merge the sp500 and Tbills data using the merge_datasets function

    data = merge_datasets(sp500_monthly, tbills_monthly)
    
    shiller_data['Date'] = shiller_data['Date'] + pd.DateOffset(months=1) - pd.DateOffset(days=1)

    
    # Merge the data dataframe with the shiller_data dataframe on the 'Date' column
    if(date != ''):
        data = data[(data['Date']>np.datetime64(date))] 

    data['Date'] = pd.to_datetime(data['Date'])
    # Merge the data dataframe with the shiller_data dataframe on the 'Date' column
    merged_data = pd.merge(data, shiller_data, on='Date')

    # Print the merged dataframe
    merged_data['simple_return'] = merged_data['P'].pct_change()
    merged_data['dividend_return'] = ((merged_data['D']/12) / merged_data['P']).shift(1)

    # Calculate cumulative returns for price
    merged_data['cum_return'] = (1 + merged_data['simple_return']).cumprod()

    # Calculate cumulative returns with dividends reinvested
    merged_data['cum_return_with_dividends'] = (1 + merged_data['simple_return'] + merged_data['dividend_return']).cumprod()
    merged_data.drop(columns=['cumulative_returns'],inplace=True)

    merged_data['market_return'] = merged_data['simple_return'] + merged_data['dividend_return']

# Calculate market volatility (standard deviation of returns)
    merged_data['volatility_market'] = merged_data['market_return'].rolling(window=12).std()

    # Drop rows with missing values (first 11 months)
    merged_data.dropna(subset=['volatility_market'], inplace=True)
    merged_data.reset_index(drop=True, inplace=True)

    return merged_data

if __name__ == '__main__':
    df = get_datasets()

