# !/usr/bin/env python
# source ~/.bash_profile
import sys
import json
import urllib.request

# Global Static Variables for calls:
LIST_BUILDER = "https://api.iextrading.com/1.0/ref-data/symbols"
NEWS_LEAD = "https://api.iextrading.com/1.0/stock/"
NEWS_TAIL = "/news"


def main():
    getStockList()
    return 0

def getStockList():
    

if __name__ == "__main__":
    sys.exit(main())