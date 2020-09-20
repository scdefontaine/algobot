# Control Center

from MarketGateway import MarketGateway
from Trader import Trader
from Strategy import Strategy

from collections import deque
import threading
import traceback
import datetime
import time
import ta
# import talib as ta
import pandas as pd
# import alpaca_trade_api as trade_api
# import json

class AlgoBot:
    def __init__(self):

        self.stocks_to_trade = ['AAPL', 'AYX']

        # Communication channels

        # helper variables
        self.isOpen = False
        self.ohlc_values = {}

        # setup strading system components
        self.gw = MarketGateway()
        self.trader = Trader(self.gw, 1)
        self.strategy = Strategy(self.gw)

    def run(self):

        # While market is open, rerun every minute
        while True:

            # Figure out when market will close
            clock = self.gw.get_clock()
            closingTime = clock.next_close.replace(tzinfo=datetime.timezone.utc).timestamp()
            currTime = clock.timestamp.replace(tzinfo=datetime.timezone.utc).timestamp()
            self.timeToClose = closingTime - currTime

            # if market isOpen, skip thread
            if not self.isOpen:
                # Wait for market to open.
                print("Waiting for market to open...")
                amo_thread = threading.Thread(target=self.awaitMarketOpen)
                amo_thread.start()
                amo_thread.join()
                print("Market opened.")

            # Close all positions when 15 minutes til market close.
            if(self.timeToClose < (60 * 15)):
                print("Market closing soon.  Closing positions.")
                self.gw.close_all_positions()

                # Run script again after market close for next trading day.
                print("Sleeping until market close (15 minutes).")
                time.sleep(60 * 15)
            else:

                # Run strategy thread
                strat_thread = threading.Thread(target=self.strategy.run_strategy)
                strat_thread.start()
                strat_thread.join()

            # sleep for 60 seconds
            time.sleep(60)


    # Await market open function
    def awaitMarketOpen(self):
      self.isOpen = self.gw.get_clock().is_open
      while(not self.isOpen):
        clock = self.gw.get_clock()
        openingTime = clock.next_open.replace(tzinfo=datetime.timezone.utc).timestamp()
        currTime = clock.timestamp.replace(tzinfo=datetime.timezone.utc).timestamp()
        timeToOpen = int((openingTime - currTime) / 60)
        print("Current Time : " + str(datetime.datetime.now()))
        print(str(timeToOpen) + " minutes til market open.")
        time.sleep(60)
        self.isOpen = self.gw.get_clock().is_open


if __name__ == '__main__':
    algobot = AlgoBot()
    algobot.run()

# EOF
