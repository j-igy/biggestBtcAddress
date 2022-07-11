# get block-chain info about the biggest 
# Bitcoin Address 1P5ZEDWTKTFGxQjZphgWPQUpe554WKDfHQ
# from bitinfocharts.com page

from datetime import datetime
import pandas as pd
import ssl
import requests
import re

ssl._create_default_https_context = ssl._create_unverified_context

url      = "https://bitinfocharts.com/bitcoin/address/1P5ZEDWTKTFGxQjZphgWPQUpe554WKDfHQ"
headers  = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}
resp     = requests.get(url, headers=headers)
dfTables = pd.read_html(resp.text)
dfTable  = dfTables[2]
dfTable  = dfTable.drop(["Block","Balance","Balance, USD @ Price", "Profit"], axis=1)
dfTable  = dfTable[: dfTable.shape[0]-1 ]
dfTable.Amount = dfTable.Amount.replace(to_replace =" BTC.*", value = "", regex = True)
dfTable.Amount = dfTable.Amount.replace(to_replace =",", value = "", regex = True)
dfTable.Amount = dfTable.Amount.astype(float).round(5)
dfTable.Time   = pd.to_datetime(dfTable.Time, format="%Y-%m-%d %H:%M:%S UTC")

# dfTable.to_csv("test.csv")
# print(dfTable)