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

def main():
    # Lock time loop to the system clock.
    
    while True:
        # Create base news feed stocker list
        getStockList()
        timer()


def timer():
    # - STATR_TIME to avoid drift after multiple iterations. An individual iteration may start slightly 
    # sooner or later depending on sleep(), timer() precision and how long it takes to execute 
    # the loop body but on average iterations always occur on the interval boundaries (even if some are skipped).
    time.sleep(30.0 -((time.time() - START_TIME) % 30.0))


def getStockList():
    # Check to see if file exists
    if os.path.isfile(SYMBOLS_PATH):
        print(os.path.getmtime(SYMBOLS_PATH))
        print(time.time())
        print(time.time() - os.path.getmtime(SYMBOLS_PATH))
        print(THIRTY_MINUTES)
        # Check if time elapsed since symbols.py modification is +30 mins
        if time.time() - os.path.getmtime(SYMBOLS_PATH) > THIRTY_MINUTES:
            # Update List
            createStockList()
            print("made new stock list")
    else:
        #Create List
        createStockList()

        
def createStockList():
    # Create new symbol.txt, w allows overwrite
    symFile = open(SYMBOLS_PATH, "w")
    symbols = getApiJson()
    # iterate through each dictonary to grab symbol and append to symbols.txt
    for i, ticker in enumerate(symbols):
        # Kept two writes on seperate lines instead of (ticker['symbol'] + /n)
        # which would create a new string in mem each time.
        symFile.write(ticker['symbol'])
        # Avoid empty space at end of symbols.txt
        if i < len(symbols) - 1:
            symFile.write("\n")


def getApiJson(url=LIST_BUILDER):
    fob = urllib.request.urlopen(url)
    # Set fob as utf-8
    data = fob.read().decode('utf-8')
    # Decode Json
    decoded = json.loads(data)
    return decoded


if __name__ == "__main__":
    sys.exit(main())