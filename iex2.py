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
APIGET_END = '/news/last/10'
START_TIME = time.time()
format = "%Y-%m-%dT%H:%M:%S"


## Global Non-Static
symbolList = None
newsList = {}


def main():
    while True:
        createSymbolList()
        updates = getUpdatedNews()
        # Only run if there are new articles
        if updates is not None:
            updates = sortArticles(updates)
            printStoreNews(updates)
        timer()


def sortArticles(updates):
    sortedUpdates = sorted(updates, key=lambda k: k['datetime']) 
    return sortedUpdates

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
    #short of installing a library to handle the headers, this is what I managed to come up with
    try:
        # Open URL as res
        res = urllib.request.urlopen(url)
        # Grab landing URL
        finalUrl = res.geturl()
        return finalUrl
    except Exception as ex:
        return "Link unavailable: " + str(ex)


def getUpdatedNews():
    global newsList
    # Set to none for no update handling
    updates = None

    for symbol in symbolList:      
        news = getApiJson(APIGET_START + symbol + APIGET_END)
        # Dumps articles that have yet to be printed into the updates list
        updates = [article for article in news if article['url'] not in newsList]
        # TODO shorten key / This updates the has been printed dic, went dic for speed
        newsList.update({article['url']: None for article in news if article['url'] not in newsList})
    return updates


def printNews(article):
    print("========= [" + readableTime(article['datetime']) + "] =========")
    print(article['source'] + ": " + article['headline'])
    print(getFinalUrl(article['url']))
    print("Tags: " + article['related'])
    print("")


def printStoreNews(updates):
    # Print News List
    for article in updates:
        printNews(article)


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


def timer():
    # To avoid drift after multiple iterations. Individual iteration may start slightly 
    # sooner or later depending on sleep(), timer() precision and how long it takes to execute 
    # the loop body but on average iterations always occur on the interval boundaries (even if some are skipped).
    time.sleep(30.0 - ((time.time() - START_TIME) % 30.0))
    # print("running now")        


if __name__ == "__main__":
    sys.exit(main())