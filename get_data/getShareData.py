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

os.makedirs('share history')

for ticker in tickers:
    request_url = f'https://simfin.com/api/v1/info/find-id/ticker/{ticker}?api-key={api_key}'
    content = requests.get(request_url)
    data = content.json()
    # print(data)
    if "error" in data or len(data) < 1:
        sim_ids.append(None)
    else:
        sim_ids.append(data[0]['simId'])


# tickers = ["AMD", "NVDA"]
print(sim_ids)

data = OrderedDict()
for idx, sim_id in enumerate(sim_ids):
    os.makedirs('share history/' + str(tickers[idx]))
    d = data[tickers[idx]] = OrderedDict({"Date" : []})
    #companyId = sim_ids[ticker]
    request_url = f'https://simfin.com/api/v1/companies/id/{sim_id}/shares/prices?api-key={api_key}'
    price_content = requests.get(request_url)
    price_data = price_content.json()

    stock_price = pd.DataFrame(price_data['priceData'])
    stock_price["closeAdj"] = pd.to_numeric(stock_price["closeAdj"])
    stock_price = stock_price[["date", "closeAdj"]]
    # data[ticker]=stock_price
    stock_price.set_index('date', inplace=True)
    stock_price.to_csv(str(tickers[idx]) + '_share_history.csv')

#stock_price_dict['INTC'].head(10)
#print(data)
#df = pd.DataFrame(data)
#print(df)