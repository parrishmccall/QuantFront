# QuantFront
Fundamental stock market valuation tools. Work in progress.
Personal project for stock market valuation. Intended for general python practice as well as practice with pandas. Divided into data download, data merging, and valuation folders. 

get_data folder downloads the data from simfin. You'll need an API key to acccess it. Several different download methods including quarterly and yearly reports as well as shares outstanding for each quarter and share price history. All fundamental data is standardized for ease of use. 

manipulateData merges the pl, bs, and cf into a single sheet for each company and gives the shares oustanding as well as the share price on the day they filed the report with the SEC. 

valuation currently computes equity value, debt value, tax rate and beta. Skips finance companies since they report differently.
