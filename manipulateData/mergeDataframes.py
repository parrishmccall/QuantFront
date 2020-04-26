import pandas as pd
import os
from datetime import datetime

def merge_everything(statements, share_price, shares_outstanding):

    all_files = get_files(statements, share_price, shares_outstanding)

    for key, value in all_files.items():

        df_statements = pd.read_csv(value[0], index_col=0)
        df_share_price = pd.read_csv(value[1])
        df_shares_outstanding = pd.read_csv(value[2])

        df_shares_outstanding['year'] = pd.DatetimeIndex(df_shares_outstanding['date']).year
        dfDate = df_shares_outstanding['year'].tolist()
        dfValue = df_shares_outstanding['value'].tolist()

        if len(dfDate) < len(df_statements.columns.values):
            continue

        values = []
        try:
            for x, y in zip(dfDate, dfValue):
                for z in df_statements.columns.values:
                    if str(x) in z:
                        values.append(str(y))
                    # else:
                    #     values.append(str(0))
            values.reverse()
            df_statements.loc['Shares outstanding'] = values
        except:
            continue

        share_prices = []
        share_prices1 = {}

        share_price_dates_dict = {}
        share_out_dates = []
        share_hist_dates = []

        for x in df_shares_outstanding['date']:
            share_out_dates.append(datetime.strptime(x, '%Y-%m-%d'))

        for x in df_share_price['date']:
            share_hist_dates.append(datetime.strptime(x, '%Y-%m-%d'))

        #print(share_hist_dates)

        zipped = zip(share_hist_dates, df_share_price['closeAdj'])
        for x, y in zipped:
            share_price_dates_dict[x] = y

        #print(share_price_dates_dict)

        for x in share_out_dates:
            if x in share_price_dates_dict.keys():
                share_prices1[x.strftime('%Y-%m-%d')] = str(share_price_dates_dict.get(x))
            else:
                share_prices1[x.strftime('%Y-%m-%d')] = str(share_price_dates_dict.get(min(share_hist_dates, key= lambda y: abs(y - x))))
        #print(share_prices1)

        try:
            for x in share_prices1:
                w = x.split('-')
                for z in df_statements.columns.values:
                    if str(w[0]) in z:
                        share_prices.append(str(share_prices1.get(x)))
                        break
            share_prices.reverse()
            df_statements.loc['Share price'] = share_prices
        except:
            print('error')

        df_statements.to_csv('Everything Merged/' + key + "_everything.csv")
        print(df_statements)

def get_files(statements, price, outstanding):

    statements1 = []
    for folder in os.listdir(statements):
        statements1.append(statements + folder)

    prices = []
    for price1 in os.listdir(price):
        prices.append(price + price1)

    out = []
    for outstand in os.listdir(outstanding):
        out.append(outstanding + outstand)

    zipped = zip(statements1, prices, out)
    list1 = [list(a) for a in zipped]

    csv_files = {}

    for folder in list1:
        for file in folder:
            for file1 in os.listdir(file):
                # base = str(count)
                directory = file.split('/')
                base = directory[1]
                if base not in csv_files:
                    csv_files[base] = []
                csv_files[base].append(file + '/' + file1)
    return csv_files



merge_everything('yearly data 2/',
                 'share price/',
                 'shares_outstanding 2/')
