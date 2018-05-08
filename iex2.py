# !/usr/bin/env python
# source ~/.bash_profile
import sys
import urllib.request
import json
import time
import datetime

# Global Static
SYMBOLS_PATH = 'symbols.txt'
APIGET_START = 'https://api.iextrading.com/1.0/stock/'
APIGET_END = '/news/last/5'
START_TIME = time.time()


## Global Non-Static
symbolList = None
newsList = {}


def main():
    while True:
        createSymbolList()
        updates = getUpdatedNews()
        printStoreNews(updates)
        timer()


def createSymbolList():
    global symbolList
    # Create list from symbols.txt
    try:
        with open(SYMBOLS_PATH, 'r') as content:
        # read().splitlines() so it removes the \n
            symbolList = content.read().splitlines()
    except Exception as ex:
        errorPrint(ex)
        print("Please create symbols.txt config file to continue")
        sys.exit()


def errorPrint(ex):
    print("Error: ", ex)


def getApiJson(url):
    try:
        fob = urllib.request.urlopen(url)
        # Set fob as utf-8
        data = fob.read().decode('utf-8')
        # Decode Json
        decoded = json.loads(data)
        return decoded
    except Exception as ex:
        errorPrint(ex)
        

def getFinalUrl(url):
    try:
        # Open URL as res
        res = urllib.request.urlopen(url)
        # Grab landing URL
        finalUrl = res.geturl()
        return finalUrl
    except Exception as ex:
        return "Link unavailable: " + str(ex)


def getUpdatedNews():
    updates = {}
    for symbol in symbolList:      
        news = getApiJson(APIGET_START + symbol + APIGET_END)
        # {key:val for val in collection}
        # TODO shorten key / If not already accounted for and conatins one of the tickers, add it
        updates.update({article['url']: article for article in news if article['url'] not in newsList})
    return updates


def printNews(value):
    print("========= [" + readableTime(value['datetime']) + "] =========")
    print(value['source'] + ": " + value['headline'])
    print(getFinalUrl(value['url']))
    print("Tags: " + value['related'])
    print("")


def printStoreNews(updates):
    # added in handling to reverse intake order on the news so it prints cronologically
    reversedList = reverseNewsList(updates)

    # Print reversed News List
    for value in reversedList:
        printNews(value)

    # Store variables
    for key, value in updates.items():
        updateNewsList(key, value)


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


def reverseNewsList(updates):
    reversedList = []
    for key, value in updates.items():
        #insert next at start of list
        reversedList.insert(0, value)
    return reversedList


def timer():
    # To avoid drift after multiple iterations. Individual iteration may start slightly 
    # sooner or later depending on sleep(), timer() precision and how long it takes to execute 
    # the loop body but on average iterations always occur on the interval boundaries (even if some are skipped).
    time.sleep(30.0 - ((time.time() - START_TIME) % 30.0))
    # print("running now")        


def updateNewsList(key, value):
    global newsList
    # Key is URL
    newsList.update({key: value['headline']})


if __name__ == "__main__":
    sys.exit(main())