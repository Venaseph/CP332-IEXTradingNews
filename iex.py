# !/usr/bin/env python
# source ~/.bash_profile
import sys
import json
import urllib.request
import os


# Global Static Variables for calls:
LIST_BUILDER = "https://api.iextrading.com/1.0/ref-data/symbols"
NEWS_LEAD = "https://api.iextrading.com/1.0/stock/"
NEWS_TAIL = "/news"


def main():
    # Create base news feed stocker list
    getStockList()
    return 0


def getStockList():
    #check to see if file exists
    if os.path.isfile('./symbols.txt'):
        print("Exists!")
    else:
        print("Doesn't Exist")
        

if __name__ == "__main__":
    sys.exit(main())