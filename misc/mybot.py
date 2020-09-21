import requests
from requests.exceptions import HTTPError
import pandas as pd
import ta
import json
import traceback
import alpaca_trade_api as tradeapi
import time
import datetime
import threading

# Alpha vantage
base_url = 'https://www.alphavantage.co/query?'
api_key = 'YY9HLANQO98K0AUO'

# alpaca
alpaca_url = "https://paper-api.alpaca.markets"
alpaca_key = "PKMCXT8TUQH0YR06LFN7"
alpaca_secret = "euc5bT52sNStFI4PDKg8hrQvrZxF/MeLQak6WEhi"

class Algobot:
    def __init__(self):
        # Create alpaca object
        self.alpaca = tradeapi.REST(alpaca_key,alpaca_secret,alpaca_url,'v2')

        # create stock list
        stock_list = ['DOMO', 'TLRY', 'SQ', 'MRO', 'AAPL', 'GM', 'SNAP', 'SHOP', 'SPLK', 'BA', 'AMZN', 'SUI', 'SUN', 'TSLA', 'CGC', 'SPWR', 'NIO', 'CAT', 'MSFT', 'PANW', 'OKTA', 'TWTR', 'TM', 'RTN', 'ATVI', 'GS', 'BAC', 'MS', 'TWLO', 'QCOM' ]
        self.allstocks = []
        for stock in stock_list:
            self.allstocks.append([stock,0])

        # helper variables
        self.buy = []
        self.buyAmount = 0
        self.blacklist = set()
        self.timeToClose = None



    def run(self):

        # First, cancel any existing orders so they don't impact our buying power.
        orders = self.alpaca.list_orders(status="open")
        for order in orders:
          self.alpaca.cancel_order(order.id)

        # Wait for market to open.
        print("Waiting for market to open...")
        marketOpen = threading.Thread(target=self.awaitMarketOpen)
        tAMO.start()
        tAMO.join()
        print("Market opened.")

        # While market is open, rerun every minute
        while True:

            # Figure out when market will close
            clock = self.alpaca.get_clock()
            closingTime = clock.next_close.replace(tzinfo=datetime.timezone.utc).timestamp()
            currTime = clock.timestamp.replace(tzinfo=datetime.timezone.utc).timestamp()
            self.timeToClose = closingTime - currTime

            if(self.timeToClose < (60 * 15)):
                # Close all positions when 15 minutes til market close.
                print("Market closing soon.  Closing positions.")
                positions = self.alpaca.list_positions()
                for position in positions:
                  if(position.side == 'long'):
                    orderSide = 'sell'
                  else:
                    orderSide = 'buy'
                  qty = abs(int(float(position.qty)))
                  respSO = []
                  tSubmitOrder = threading.Thread(target=self.submitOrder(qty, position.symbol, orderSide, respSO))
                  tSubmitOrder.start()
                  tSubmitOrder.join()

                # Run script again after market close for next trading day.
                print("Sleeping until market close (15 minutes).")
                time.sleep(60 * 15)
            else:
                # Run Strategy
                stratThread = threading.Thread(target=self.run_strategy)
                stratThread.start()
                stratThread.join()
                time.sleep(60)

                # Rebalance the portfolio.
                # tRebalance = threading.Thread(target=self.rebalance)
                # tRebalance.start()
                # tRebalance.join()
                # time.sleep(60)

    # Run Strategy
        # Rules
            # allowed 3 trades over a 5 business day span
            # must make at least 5% a week
            # cannot hold overnight
            # cannot risk more than 50% of portfolio value
            # high enough 14 day avg volume to gain at least 5% in a day
            # positive directional movement (+DI)
            # strong directional movement (ADX)
            # 14 day rate of change (roc) must be above 0%
            #
    def run_strategy(self):
        # get the stock data and rank by rsi values
            # add indicator weights based on number of buy signals
        rankings = threading.Thread(target=self.rerank)
        rankings.start()
        rankings.join()

        # Clear existing orders again
        orders = self.alpaca.list_orders(status="open")
        for order in orders:
          self.alpaca.cancel_order(order.id)

        print("Taking position in: " + str(self.buy))

        # Remove positions no longer in the top 5

        positions = self.alpaca.list_positions()
        for position in positions:
            # if position is not in top 5, sell it's position
            if(self.buy.count(position.symbol) == 0):
                #

            # if position in top 5, buy allocated amounts
            else:
                #

    # re-rank all stocks by indicator values (possibly add value weights based on number of buy signals a stock has)
    def rerank(self):
        rank = threading.Thread(target=self.rank)
        rank.start()
        rank.join()

        # Grab the top 5 ranked stocks
        top_ranked = [[],[],[],[],[]]

        # Split equity evenly between top 5 - aka 20% each
        equity = int(float(self.alpaca.get_account().equity))
        self.buyAmount = 0.2

        respGetBuy = []
        getBuy = threading.Thread(target=self.getTotalPrice, args=[self.buy,respGetBuy])
        getBuy.start()
        getBuy.join()

        self.buy = int(self.buyAmount // respGetBuy[0])

    # ranks the stocks by indicator values
    def rank(self):
        getRSI = threading.Thread(target=self.getRSI)
        getRSI.start()
        getRSI.join()

        # sort the stocks by rsi values


    # get total price for array of stocks
    def getTotalPrice(self, stocks, resp):
        totalPrice = 0
        for stock in stocks:
            bars = self.alpaca.get_barset(stock,"minute",1)
            totalPrice+= bars[stock][0].c
        resp.append(totalPrice)

    # get the rsi values for the past 10 minutes
    def getRSI(self):
        # set the parameters
        close = ''                      # pull close data from df
        period = 14
        fillna = false                  # required parameter, dont change
        # load symbol & rsi values into array
        for i, stock in enumerate(self.allStocks):
            # get close price for each stock
            bars = self.alpaca.get_barset(stock[0], "minute", length)
            self.allstocks[i][1] = (bars[stocks[0]][len(bars[stock[0]]) - 1].c - bars[stock[0]].o) / bars[stock[0]][0].o
            # get rsi value based on close price for each stock
            rsi_df = ta.RSIIndicator(close,period,fillna)

    # Wait for market to open.
    def awaitMarketOpen(self):
      isOpen = self.alpaca.get_clock().is_open
      while(not isOpen):
        clock = self.alpaca.get_clock()
        openingTime = clock.next_open.replace(tzinfo=datetime.timezone.utc).timestamp()
        currTime = clock.timestamp.replace(tzinfo=datetime.timezone.utc).timestamp()
        timeToOpen = int((openingTime - currTime) / 60)
        print(str(timeToOpen) + " minutes til market open.")
        time.sleep(60)
        isOpen = self.alpaca.get_clock().is_open

    def submitOrder(self, qty, stock, side, resp):
        if(qty > 0):
          try:
            self.alpaca.submit_order(stock, qty, side, "market", "day")
            print("Market order of | " + str(qty) + " " + stock + " " + side + " | completed.")
            resp.append(True)
          except:
            print("Order of | " + str(qty) + " " + stock + " " + side + " | did not go through.")
            resp.append(False)
        else:
          print("Quantity is 0, order of | " + str(qty) + " " + stock + " " + side + " | not completed.")
          resp.append(True)


# Run Algobot class
algobot = Algobot()
algobot.run()
