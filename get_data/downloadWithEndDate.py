import requests
import pandas as pd
from collections import OrderedDict
import os
from collections import OrderedDict

#global api_key,sim_id_dict,stock_price_dict
# here you have to enter your actual API key from SimFin
api_key = "*"

sim_ids = []
stock_price_dict={}
#tickers = ['AAPL', 'MSFT']
df2 = pd.read_csv('stocks_list.csv')
tickers = df2.columns.values[:21]

statement_type = ['pl', 'bs', 'cf']
#time_periods = ["Q1", "Q2", "Q3", "Q4"]
time_periods = ["FY"]
year_start = 2013
year_end = 2018

#os.makedirs('shares outstanding')

for ticker in tickers:
    request_url = f'https://simfin.com/api/v1/info/find-id/ticker/{ticker}?api-key={api_key}'
    content = requests.get(request_url)
    data = content.json()
    # print(data)
    if "error" in data or len(data) < 1:
        sim_ids.append(None)
    else:
        sim_ids.append(data[0]['simId'])

print(sim_ids)

data = OrderedDict()
for idx, sim_id in enumerate(sim_ids):
    os.makedirs('period end date/' + str(tickers[idx]))
    d = data[tickers[idx]] = OrderedDict({"Period End Date" : []})
    request_url = f'https://simfin.com/api/v1/companies/id/{sim_id}/statements/standardised?stype={statement}&fyear={year}&ptype={time_period}&api-key={api_key}    shares_content = requests.get(request_url)
    shares_data = shares_content.json()

    stock_price = pd.DataFrame(shares_data)
    #stock_price["closeAdj"] = pd.to_numeric(stock_price["closeAdj"])
    # data[ticker]=stock_price
    stock_price.set_index('date', inplace=True)
    stock_price.to_csv(str(tickers[idx]) + '_shares_outstanding.csv')