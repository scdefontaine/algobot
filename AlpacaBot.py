# Alpaca Bot

from MarketGateway import MarketGateway
from Trader import Trader
from Strategy import Strategy

import threading
import traceback
import datetime
import time

class AlgoBot:
    def __init__(self):

        # input from sentiment bot
        self.stocks_to_trade = self.get_stocks()

        # helper variables
        self.isOpen = False

        # setup strading system components
        self.gw = MarketGateway()
        self.trader = Trader(self.gw, 1)
        self.strategy = Strategy(self.gw, stocks_to_trade, trader)

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

            else:
                # Run strategy thread
                strat_thread = threading.Thread(target=self.strategy.run)
                strat_thread.start()
                strat_thread.join()

            # sleep for 60 seconds
            time.sleep(60)

    # Get stocks from sentiment bot
    def get_stocks(self):
        return ['AAPL','AYX']

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
