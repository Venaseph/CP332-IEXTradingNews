# !/usr/bin/env python
# source ~/.bash_profile
import sys
import json
import urllib.request
import os
import datetime
import time


# Global Static Variables:
LIST_BUILDER = 'https://api.iextrading.com/1.0/ref-data/symbols'
NEWS_LEAD = 'https://api.iextrading.com/1.0/stock/'
NEWS_TAIL = '/news'
SYMBOLS_PATH = 'symbols.txt'
THIRTY_MINUTES = 30 * 60
START_TIME = time.time()

# Global Non-Static
symbolList = None


def main():
    # Lock time loop to the system clock.
    
    while True:
        # Create base news feed stocker list, or update .txt & list when needed.
        getStockList()
        getNews()
        timer()


def getNews():
    for symbol in symbolList:
        print(symbol)


def createSymbolList():
    global symbolList
    # Create list from symbols.txt
    with open(SYMBOLS_PATH, 'r') as content:
        # read().splitlines() so it removes the \n
        symbolList = content.read().splitlines()
    return symbolList


def getStockList():
    # Check to see if file exists
    if os.path.isfile(SYMBOLS_PATH):
        # Check if time elapsed since symbols.py modification is +30 mins
        if time.time() - os.path.getmtime(SYMBOLS_PATH) > THIRTY_MINUTES:
            # Update List/.txt
            createStockTxt()
            createSymbolList()
            # print("Made new stock list")
    else:
        #Create List/.txt
        createStockTxt()
        createSymbolList()

        
def createStockTxt():
    # Create new symbol.txt, w allows overwrite
    with open(SYMBOLS_PATH, 'w') as content:
        #get decoded json
        symbols = getApiJson()
        # iterate through each dictonary to grab symbol and append to symbols.txt
        for i, ticker in enumerate(symbols):
            # Kept two writes on seperate lines instead of (ticker['symbol'] + /n)
            # which would create a new string in mem each time.
            content.write(ticker['symbol'])
            # Avoid empty space at end of symbols.txt
            if i < len(symbols) - 1:
                content.write("\n")


def getApiJson(url=LIST_BUILDER):
    try:
        fob = urllib.request.urlopen(url)
        # Set fob as utf-8
        data = fob.read().decode('utf-8')
        # Decode Json
        decoded = json.loads(data)
        return decoded
    except Exception as ex:
        errorPrint(ex)


def errorPrint(ex):
    print("Error: ", ex)
    sys.exit()


def timer():
    # - START_TIME to avoid drift after multiple iterations. An individual iteration may start slightly 
    # sooner or later depending on sleep(), timer() precision and how long it takes to execute 
    # the loop body but on average iterations always occur on the interval boundaries (even if some are skipped).
    time.sleep(30.0 - ((time.time() - START_TIME) % 30.0))

if __name__ == "__main__":
    sys.exit(main())