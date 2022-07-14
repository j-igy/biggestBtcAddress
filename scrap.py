from asyncio.windows_events import NULL
from cmath import nan
from statistics import mode
import pandas as pd
import ssl, json, re
import requests
from utility import logging, saveObjToFile, saveToFile


# get block-chain info about the biggest 
# Bitcoin Address 1P5ZEDWTKTFGxQjZphgWPQUpe554WKDfHQ
# from bitinfocharts.com page
class biggestBtcAddress:

    def __init__(self, addresses:list=NULL, onlyPrivate:bool=True):
        self.log = logging("biggestBtcAddress")
        self.log.INFO()
        self.__urlPrefix         = "https://bitinfocharts.com/"
        self.__adrsBalances:dict = self.getBalanceForThis(addresses) if addresses else self.getTop100(onlyPrivate)
        self.__image:dict        = self.getTransactionTablesFor(self.__adrsBalances)

    def getImage(self):
        return self.__image

    def getAddressesBalances(self):
        return self.__adrsBalances

    def saveImageToFile(self, fileName="Image.csv"):
        self.log.INFO()
        saveToFile("", fileName, mode="w")
        for x in self.__image:
            saveToFile(x, fileName, mode="a")
            self.__image[x].to_csv( fileName, mode="a")

    def getBalanceForThis(self, addresses:list) -> dict:
        self.log.INFO()
        balance = {}
        for adr in addresses:
            self.log.INFO(adr)
            transactions, balance[adr] = self.getTransactionTableFor(adr) 
        return balance

    def getBalance(self, adr):
        self.log.INFO()
        return 20.9

    def getTransactionTablesFor(self, addresses:dict):
        self.log.INFO()
        transactions = {}
        for adr in addresses:
            self.log.INFO(adr)
            transactions[adr], balance = self.getTransactionTableFor(adr)
        return transactions

    # Get tables from webpage
    def getTablesFromHtml(self, url) -> list: 
        self.log.INFO()
    
        # Create a https context
        # ssl._create_default_https_context = ssl._create_unverified_context
        
        # Request page
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}
        url     = self.__urlPrefix + url
        resp    = requests.get(url, headers=headers)

        # Return the converted html table to the list of pandas DFs
        return pd.read_html(resp.text)


    # Get a table with the last operations from the page
    def getTransactionTableFor(self, address) -> pd.DataFrame: 
        self.log.INFO()

        # From the list of DFs, get the third DF - it contains the necessary data
        dfTables = self.getTablesFromHtml("bitcoin/address/" + address)
        transactions = dfTables[2]

        # Remove unnecessary columns and row
        transactions = transactions.drop(["Block","Balance","Balance, USD @ Price", "Profit"], axis=1)
        transactions = transactions[: transactions.shape[0]-1 ]

        # convert the "Amont" col to float type
        transactions.Amount = transactions.Amount.replace(to_replace =" BTC.*", value = "", regex = True)
        transactions.Amount = transactions.Amount.replace(to_replace =",", value = "", regex = True)
        transactions.Amount = transactions.Amount.astype(float).round(5)

        # convert the "Time" col to float type
        transactions.Time   = pd.to_datetime(transactions.Time, format="%Y-%m-%d %H:%M:%S UTC")

        balance = dfTables[1][0][0]
        balance = re.sub(" BTC.*", "", balance)
        balance = re.sub("Balance: ", "", balance)
        balance = re.sub("[\.].*", "", balance)
        balance = re.sub(",", "", balance)
        balance = float(balance)

        return transactions, balance


    # Update the table, return new position in the table as DF
    def checkChanges(self):
        self.log.INFO()
        # newAdrsBalances = self.getBalanceForThis(self.__adrsBalances)

    # Get a table with the last operations from the page
    def getTop100(self, onlyPrivate:bool=False, pageNo=1) -> dict:
        self.log.INFO()

        # Get html tables from page as list of pandas DFs
        url = ("top-100-richest-bitcoin-addresses-%d.html" % pageNo)
        dfTables = self.getTablesFromHtml(url)

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
        if onlyPrivate: 
            dfTable = dfTable.fillna(0)
            dfTable = dfTable[dfTable["Info"] == 0]
            dfTable = dfTable.reset_index()
        
        # convert to dict
        dfTable = dfTable.set_index("Address")
        dfTable = dfTable.drop(["pos", "Info"], axis=1)
        addressBalances = dfTable.to_dict()["Balance"]

        return addressBalances

adrs = ["1P5ZEDWTKTFGxQjZphgWPQUpe554WKDfHQ", "bc1qazcm763858nkj2dj986etajv6wquslv8uxwczt", "1FeexV6bAHb8ybZjqQMjJrcCrHGW9sb6uF"]
address = biggestBtcAddress(adrs)

saveObjToFile("test.json", address.getAddressesBalances())
address.saveImageToFile()






