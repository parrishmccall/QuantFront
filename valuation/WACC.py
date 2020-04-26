import pandas as pd
import os
from sklearn.linear_model import LinearRegression
import numpy as np
import statsmodels.api as sm
from statsmodels import regression
from sklearn.preprocessing import StandardScaler
from scipy.stats import linregress
from scipy import stats
import decimal
from datetime import  datetime, timedelta
import math


# TODO make sure finance companies don't end up in this dataset
# Prevent by looking for long term securities in index

def compute_equity_value(input_dir):

    files = []
    for x in os.listdir(input_dir):
        files.append('data/' + x)

    for file in files:
        df = pd.read_csv(file, index_col=0)
        #print(df)

        shares = []
        for x in df.columns.values:
            shares.append(df.get_value('Share price', x))
        #print(shares)

        shares_out = []
        for x in df.columns.values:
            shares_out.append(df.get_value('Shares outstanding', x))
        zipped = zip(shares, shares_out)

        value = []
        for x,y in zipped:
            value.append(x*y)
        df.loc['Equity Value'] = value
        #print(df)
        df.to_csv(file)

        #print(value)

def compute_debt_value(input_dir):
    files = []
    for x in os.listdir(input_dir):
        files.append('data/' + x)

    for file in files:
        df = pd.read_csv(file, index_col=0)
        if 'Long Term Marketable Securities' not in df.index:
            continue
        else:

            cash = []
            for x in df.columns.values:
                cash.append(df.get_value('Cash & Cash Equivalents', x))


            securities = []
            for x in df.columns.values:
                securities.append(df.get_value('Long Term Marketable Securities', x))


            short_term_debt = []
            for x in df.columns.values:
                short_term_debt.append(df.get_value('Short Term Debt', x) + df.get_value('Current Portion of Long Term Debt', x))


            long_term_debt = []
            for x in df.columns.values:
                long_term_debt.append(df.get_value('Long Term Debt', x))


            zipped = zip(cash, securities, short_term_debt, long_term_debt)

            debt_value = []
            for cash, sec, short, long in zipped:
                debt_value.append(long + short - cash - sec)
            df.loc['Debt Value'] = debt_value
            df.to_csv(file)


def compute_tax_rate(input_dir):
    files = []
    for x in os.listdir(input_dir):
        files.append('data/' + x)

    for file in files:
        df = pd.read_csv(file, index_col=0)
        if 'Long Term Marketable Securities' not in df.index:
            continue
        else:

            pretax_income = []
            for x in df.columns.values:
                pretax_income.append(df.get_value('Pretax Income (Loss)', x))

            income_tax_expense = []
            for x in df.columns.values:
                y = df.get_value('Income Tax (Expense) Benefit, net', x)
                income_tax_expense.append(abs(y))


            zipped = zip(pretax_income, income_tax_expense)

            tax_rate = []
            for x, y in zipped:
                tax_rate.append(y / x)
            df.loc['Tax Rate'] = tax_rate
            df.to_csv(file)


def compute_beta(input_dir): # Computes based on daily closing price

    df1 = pd.read_csv('share price/AAPL/AAPL_share_history.csv', index_col = 'date', parse_dates=True, usecols=['date', 'closeAdj'])
    df1 = df1.rename(columns={'closeAdj': 'AAPL'})

    df = pd.read_csv('SPY.csv',  index_col = 'date', parse_dates=True, usecols=['date', 'closeAdj'])
    df = df.rename(columns={'closeAdj': 'SPY'})

    df = df.groupby(pd.TimeGrouper('M')).nth(0)
    #print(df)

    df1 = df1.groupby(pd.TimeGrouper('M')).nth(0)
    #print(df1)

    df2 = df1.join(df)
    df2 = df2.dropna(axis=0)
    #print(df2)

    df2['dates'] = df2.index.values
    spy = df2['SPY'].values
    spy = spy[::-1]
    #print(spy)
    spy_returns = []
    count = 0
    for x in spy:
        try:
            spy_returns.append((x-spy[count+1])/spy[count+1])
            count += 1
        except:
            print('error')
    #print(spy_returns)

    stock = df2['AAPL'].values
    stock = stock[::-1]
    #print(stock)
    stock_returns = []
    count = 0
    for x in stock:
        try:
            stock_returns.append((x-stock[count+1])/stock[count+1])
            count += 1
        except:
            print('error')

    cov = np.cov(spy_returns, stock_returns, bias=True)
    print(cov[0][1])
    var = np.var(spy_returns, ddof=1)
    print(var)

    beta = cov[0][1]/var
    print(beta)



# def compute_beta(input_dir): #test with linear regression
#     df = pd.read_csv('SPY.csv', index_col='date', parse_dates=True, usecols=['date', 'closeAdj'])
#     df = df.rename(columns={'closeAdj': 'SPY'})
#     # print(df)
#     df1 = pd.read_csv('share price/ADBE/ADBE_share_history.csv', index_col='date', parse_dates=True, usecols=['date', 'closeAdj'])
#     # df1 = df1.drop(['Open', "High", 'Low', 'Close', 'Volume'], axis=1)
#     df1 = df1.rename(columns={'closeAdj': 'ADBE'})
#     #print(df1)
#     df2 = df1.join(df)
#     df2 = df2.dropna(axis=0)
#     #print(df2)
#
#     X = df2[['SPY']].values
#     X = X[::-1]
#     print(X)
#     y = df2[['ADBE']].values
#     y = y[::-1]
#     print(y)
#
    # reg = LinearRegression().fit(X,y)
    # print(reg.coef_)

# def compute_beta(input_dir): #test with linear regression
#     df = pd.read_csv('SPY.csv', index_col='date', parse_dates=True, usecols=['date', 'closeAdj'])
#     df = df.rename(columns={'closeAdj': 'SPY'})
#     # print(df)
#     df1 = pd.read_csv('share price/AAPL/AAPL_share_history.csv', index_col='date', parse_dates=True,
#                       usecols=['date', 'closeAdj'])
#     # df1 = df1.drop(['Open', "High", 'Low', 'Close', 'Volume'], axis=1)
#     df1 = df1.rename(columns={'closeAdj': 'AAPL'})
#     #print(df1)
#     df2 = df1.join(df)
#     df2 = df2.dropna(axis=0)
#     print(df2)
#     y = df2[['AAPL']].values
#     X = df2[['SPY']].values
#
#     # def lin_reg(x,y):
#     #     x = sm.add_constant(x)
#     #     model = regression.linear_model.OLS(y,x).fit()
#     #     x = x[:,1]
#     #     return model.params[0], model.params[1]
#     # alpha, beta = lin_reg(y, X)
#     X1 = sm.add_constant(X)
#     model = sm.OLS(y, X1)
#     results = model.fit()
#
#     print(results.summary())



# def compute_beta(statements, share_price, shares_out):
#
#     shares_folders =  []
#     for folder in os.listdir(share_price):
#         shares_folders.append(share_price + folder)
#     #print(shares_folders)
#
#     files = get_files(statements, share_price, shares_out)
#     print(files)

    # shares_files = {}
    # for folder in shares_folders:
    #     for file in os.listdir(folder):
    #         base = folder + '/'
    #         if base not in shares_files:
    #             shares_files[base] = []
    #         shares_files[base].append(folder + '/' + file)
    # #print(shares_files)
    #
    # df_spy = pd.read_csv('share price/SPY/SPY_share_history.csv')
    # df_spy['date'] = pd.DatetimeIndex(df_spy['date'])
    # print(df_spy)
    # for file in shares_files.values():
    #     #print(file)
    #     df_share_price = pd.read_csv(file[0])
    #     df_share_price['date'] = pd.DatetimeIndex(df_share_price['date'])




# def get_files(statements, share_price, shares_out):
#     statements = []
#     for folder in statements:
#         statements.append(str(folder))
#
#     share_price2 = []
#     for price in os.listdir(share_price):
#         share_price2.append(share_price + '/' + price)
#
#     shares_outstanding2 = []
#     for outstand in os.listdir(shares_out):
#         shares_outstanding2.append(shares_out + '/' + outstand)
#
#     zipped = zip(share_price2, shares_outstanding2)
#     list1 = [list(a) for a in zipped]
#     print(list1)
#     #list2 = zip(list1, statements)
#
#     csv_files = {}
#
#     for folder in list1:
#         for file in folder:
#             for file1 in os.listdir(file):
#                 directory = file.split('/')
#                 base = directory[1]
#                 if base not in csv_files:
#                     csv_files[base] = []
#                 csv_files[base].append(file + '/' + file1)
#
#
#     return csv_files



compute_beta('data/')