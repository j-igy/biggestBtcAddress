import pandas as pd
import ssl
import requests


# get block-chain info about the biggest 
# Bitcoin Address 1P5ZEDWTKTFGxQjZphgWPQUpe554WKDfHQ
# from bitinfocharts.com page
class biggestBtcAddress:

    def __init__(self, address:str):
        self.urlPrefix = "https://bitinfocharts.com/bitcoin/address/"
        self.address   = address
        self.df        = self.getTransactionTable()
    
    # Get a table with the last operations from the page
    def getTransactionTable(self):
    
        # Create a https context
        # ssl._create_default_https_context = ssl._create_unverified_context
        
        # Request page
        url      = self.urlPrefix + self.address
        headers  = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}
        resp     = requests.get(url, headers=headers)

        # Convert html table to the list of pandas DFs
        dfTables = pd.read_html(resp.text)

        # From the list of DFs, get the third DF - it contains the necessary data
        dfTable  = dfTables[2]

        # Remove unnecessary columns and row
        dfTable  = dfTable.drop(["Block","Balance","Balance, USD @ Price", "Profit"], axis=1)
        dfTable  = dfTable[: dfTable.shape[0]-1 ]

        # convert the "Amont" col to float type
        dfTable.Amount = dfTable.Amount.replace(to_replace =" BTC.*", value = "", regex = True)
        dfTable.Amount = dfTable.Amount.replace(to_replace =",", value = "", regex = True)
        dfTable.Amount = dfTable.Amount.astype(float).round(5)

        # convert the "Time" col to float type
        dfTable.Time   = pd.to_datetime(dfTable.Time, format="%Y-%m-%d %H:%M:%S UTC")

        return dfTable


    # Update the table, return new position in the table as DF
    def checkChanges(self, greaterThan:float=0.0 ):
        # Symulation of the new data
        # self.df = self.df[3:].reset_index(drop=True)

        # Get the newest table 
        newDf   = self.getTransactionTable()

        # Select new row
        dfDelta = pd.concat([newDf, self.df])
        dfDelta = dfDelta.drop_duplicates(keep=False, ignore_index=True)
        dfDelta = dfDelta[dfDelta.Amount > greaterThan]

        # update dataframe
        self.df = newDf

        return dfDelta
        

addres = biggestBtcAddress("1P5ZEDWTKTFGxQjZphgWPQUpe554WKDfHQ")
deltaDf = addres.checkChanges(5)
if not deltaDf.empty:
    deltaDf = deltaDf.to_string(index=False)
    print((deltaDf))

# deltaDf.to_csv("test.csv")
# print(deltaDf)




