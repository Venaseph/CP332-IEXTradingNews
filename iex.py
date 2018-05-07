# !/usr/bin/env python
# source ~/.bash_profile
import sys
import json
import urllib.request
import os
import datetime
import time


# Global Static:
LIST_BUILDER = 'https://api.iextrading.com/1.0/ref-data/symbols'
NEWS_API = 'https://api.iextrading.com/1.0/stock/market/news/last/100'
SYMBOLS_PATH = 'symbols.txt'
THIRTY_MINUTES = 30 * 60
START_TIME = time.time()

# Global Non-Static
symbolList = None
newsList = {}


def main():
    
    while True:
        getStockList()
        updates = getUpdatedNews()
        printStoreNews(updates)
        timer()


def printStoreNews(updates):
    # added in handling to reverse intake order on the news so it prints cronologically
    reversedList = reverseNewsList(updates)

    # Print reversed News List
    for value in reversedList:
        printNews(value)

    # Store variables
    for key, value in updates.items():
        updateNewsList(key, value)
        

def reverseNewsList(updates):
    reversedList = []
    for key, value in updates.items():
        #insert next at start of list
        reversedList.insert(0, value)
    return reversedList


def printNews(value):
    print("========= [" + readableTime(value['datetime']) + "] =========")
    print(value['source'] + ": " + value['headline'])
    print(getFinalUrl(value['url']))
    print("Tags: " + value['related'])
    print("")


def readableTime(ts):
    try:
        # Create intake format
        format = "%Y-%m-%dT%H:%M:%S"
        # Make strptime obj from string minus the crap at the end
        strpTime = datetime.datetime.strptime(ts[:-6], format)
        # Create string of the pieces I want from obj
        convertedTime = strpTime.strftime("%B %d %Y, %-I:%m %p")
        return convertedTime
    except Exception as ex:
        return "Datetime not available: " + str(ex)

def getFinalUrl(url):
    try:
        res = urllib.request.urlopen(url)
        finalUrl = res.geturl()
        return finalUrl
    except Exception as ex:
        return "Link unavailable: " + str(ex)


def updateNewsList(key, value):
    global newsList
    # Key is URL
    newsList.update({key: value['headline']})

def getUpdatedNews():
    updates = {}
    news = getApiJson(NEWS_API)
    # {key:val for val in collection}
    # TODO shorten key / If not already accounted for and conatins one of the tickers, add it
    updates.update({article['url']: article for article in news if article['url'] not in newsList for symbol in symbolList if ("," + symbol + "," or symbol + "," or "," + symbol) in article['related']})
    return updates
            

def createSymbolList():
    global symbolList
    # Create list from symbols.txt
    with open(SYMBOLS_PATH, 'r') as content:
        # read().splitlines() so it removes the \n
        symbolList = content.read().splitlines()


def getStockList():
    # Check to see if file exists
    if os.path.isfile(SYMBOLS_PATH):
        # Check if time elapsed since symbols.py modification is +30 mins or symbolList isn't populated
        if (time.time() - os.path.getmtime(SYMBOLS_PATH) > THIRTY_MINUTES or symbolList == None):
            # Update List/.txt
            createStockTxt()
            createSymbolList()
            #print("Made new stock list")
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
            if "#" not in ticker['symbol']:
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


def timer():
    # To avoid drift after multiple iterations. Individual iteration may start slightly 
    # sooner or later depending on sleep(), timer() precision and how long it takes to execute 
    # the loop body but on average iterations always occur on the interval boundaries (even if some are skipped).
    time.sleep(30.0 - ((time.time() - START_TIME) % 30.0))
    # print("running now")


if __name__ == "__main__":
    sys.exit(main())