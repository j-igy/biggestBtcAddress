from cmath import nan
import pandas as pd
import ssl
import requests


# get block-chain info about the biggest 
# Bitcoin Address 1P5ZEDWTKTFGxQjZphgWPQUpe554WKDfHQ
# from bitinfocharts.com page
class biggestBtcAddress:

    def __init__(self, address:str="", onlyPrivate:bool=True):
        self.__urlPrefix   = "https://bitinfocharts.com/"
        self.__headers     = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}
        self.__onlyPrivAdr = onlyPrivate
        self.__address     = self.setBtcAddress(address)
        self.__df          = self.getTransactionTable(self.__address)
    
    def getDf(self):
        return self.__df
    
    def setBtcAddress(self, address:str):
            return self.getTop100(True).Address[0] if not address else address

    # Get a table with the last operations from the page
    def getTransactionTable(self, address):
    
        # Create a https context
        # ssl._create_default_https_context = ssl._create_unverified_context
        
        # Request page
        url      = self.__urlPrefix + "bitcoin/address/" + address
        resp     = requests.get(url, headers=self.__headers)

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
        # self.__df = self.__df[3:].reset_index(drop=True)

        # Get the newest table 
        newDf   = self.getTransactionTable(self.__address)

        # Select new row
        dfDelta = pd.concat([newDf, self.__df])
        dfDelta = dfDelta.drop_duplicates(keep=False, ignore_index=True)
        dfDelta = dfDelta[dfDelta.Amount > greaterThan]

        # update dataframe
        self.__df = newDf

        return dfDelta

    # Get a table with the last operations from the page
    def getTop100(self, onlyPrivate:bool=False):
    
        # Create a https context
        # ssl._create_default_https_context = ssl._create_unverified_context
        
        # Request page
        url      = self.__urlPrefix + "top-100-richest-bitcoin-addresses.html"
        resp     = requests.get(url, headers=self.__headers)

        # Convert html table to the list of pandas DFs
        dfTables = pd.read_html(resp.text)

        # Get table from the list of DFs
        dfTable = []
        dfTable.append(dfTables[2])
        dfTable.append(dfTables[3])
        dfTable[0] = dfTable[0].rename(columns={"Unnamed: 0":"pos"}).set_index("pos")
        dfTable[1] = dfTable[1].rename(columns={0:"pos"}).set_index("pos")
        dfTable[1].columns = dfTable[0].columns
        dfTable = pd.concat([dfTable[0], dfTable[1]])
        dfTable = dfTable.rename(columns={"Balance △1w/△1m":"Balance"})
        
        # Remove unnecessary columns and row
        dfTable  = dfTable.drop(["% of coins","First In","Last In","Ins","First Out","Last Out","Outs"], axis=1)

        # clear data
        dfTable.Address = dfTable.Address.replace(to_replace ="wallet:", value = "", regex = True)
        dfTable.Address = dfTable.Address.replace(to_replace ="[\.]+", value = "", regex = True)
        dfTable["Info"] = nan
        dfTable.Info    = dfTable.Address.str.extract(r"( .*)")
        dfTable.Address = dfTable.Address.replace(to_replace =" .*", value = "", regex = True)
        
        dfTable.Balance = dfTable.Balance.replace(to_replace =" BTC.*", value = "", regex = True)
        dfTable.Balance = dfTable.Balance.replace(to_replace =",", value = "", regex = True)
        dfTable.Balance = dfTable.Balance.astype(float).round(1)
        
        # drop institutional address
        if self.__onlyPrivAdr: 
            dfTable = dfTable.fillna(0)
            dfTable = dfTable[dfTable["Info"] == 0]
            dfTable = dfTable.reset_index()

        return dfTable


address = biggestBtcAddress()
df = address.getDf()
df.to_csv("test.csv")

deltaDf = address.checkChanges(5)
if not deltaDf.empty:
    deltaDf = deltaDf.to_string(index=False)
    print((deltaDf))




