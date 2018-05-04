# !/usr/bin/env python
# source ~/.bash_profile
import sys
import json
import urllib.request
import os
import datetime
import time


# Global Static Variables for calls:
LIST_BUILDER = 'https://api.iextrading.com/1.0/ref-data/symbols'
NEWS_LEAD = 'https://api.iextrading.com/1.0/stock/'
NEWS_TAIL = '/news'
SYMBOLS_PATH = './symbols.txt'
THIRTY_MINUTES = 10 * 60 * 1000


def main():
    # Create base news feed stocker list
    getStockList()
    return 0


def getStockList():
    # Check to see if file exists
    if os.path.isfile(SYMBOLS_PATH):
        # Check if time elapsed since symbols.py modification is +30 mins
        if os.path.getmtime(SYMBOLS_PATH) < (THIRTY_MINUTES):
            # Update List
            createStockList()
            print("made new stock list")
    else:
        #Create List
        createStockList()

        
def createStockList():
    # Create new symbol.txt, w allows overwrite
    symFile = open("symbols.txt", "w")
    # Open the URL url, which can be either a string or a Request object
    fob = urllib.request.urlopen(LIST_BUILDER)
    # Decode fob
    data = fob.read().decode('utf-8')
    # load json data from fob
    symbols = json.loads(data)
    # iterate through each dictonary to grab symbol and append to symbols.txt
    for ticker in symbols:
        # Kept two writes on seperate lines instead of (ticker['symbol'] + /n)
        # which would create a new string in mem each time it runs.
        symFile.write(ticker['symbol'])
        symFile.write("\n")


if __name__ == "__main__":
    sys.exit(main())