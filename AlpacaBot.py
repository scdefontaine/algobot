# Alpaca Bot

from MarketGateway import MarketGateway

import threading
import traceback
import datetime
import time
import pandas as pd
from datetime import timedelta
import matplotlib.pyplot as plt
import ta
import numpy as np
import sys,os
import logging
from dateutil.relativedelta import relativedelta
from IPython.display import display
import matplotlib.cbook as cbook
import matplotlib.gridspec as gridspec
from matplotlib.ticker import Formatter
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

class AlgoBot:

    def __init__(self):

        # input from sentiment bot
        # self.stocks_to_trade = ['AAPL','TSLA','ORCL','AYX','MDB']
        self.stocks_to_trade = open("sp500_tickers.txt", "r").read().split("\n")

        # helper variables
        self.isOpen = False

        # setup trading system components
        self.gate = MarketGateway()

    def SMA(self,close,sPeriod,lPeriod):
        shortSMA = ta.trend.sma_indicator(close,sPeriod)
        longSMA = ta.trend.sma_indicator(close,lPeriod)
        smaSell = ((shortSMA <= longSMA)) #& (shortSMA.shift(1) >= longSMA.shift(1)))
        smaBuy = ((shortSMA >= longSMA)) #& (shortSMA.shift(1) <= longSMA.shift(1)))
        return smaSell,smaBuy,shortSMA,longSMA

    def RSI(self,close,timePeriod):
        rsi = ta.momentum.rsi(close,timePeriod)
        rsiSell = (rsi>70) #& (rsi.shift(1)<=70)
        rsiBuy = (rsi<30) #& (rsi.shift(1)>=30)
        return rsiSell,rsiBuy, rsi

    def Stoch(self,close,high,low):
        slowk = ta.momentum.stoch(high, low, close)
        slowd = ta.momentum.stoch_signal(high, low, close)
        stochSell = ((slowk < slowd) & (slowd > 80)) # & (slowk.shift(1) > slowd.shift(1)))
        stochBuy = ((slowk > slowd) & (slowd < 20)) # & (slowk.shift(1) < slowd.shift(1)))
        return stochSell,stochBuy, slowk,slowd

    # Function used for real time analysis
    def runAllTA(self,ticker, data):

        print("Running ta...")
        price = data[ticker]['close']
        high = data[ticker]['high']
        low = data[ticker]['low']

        # Simple Moving Average calcs
        smaSell,smaBuy,shortSMA,longSMA = SMA(price,shortPeriod,longPeriod)
        # Do the RSI calcs
        rsiSell,rsiBuy,rsi = RSI(price,shortPeriod)
        # and now the stochastics
        stochSell,stochBuy,slowk,slowd = Stoch(price, high, low)

        # Now collect buy and sell Signal timestamps into a single df
        sigTimeStamps = pd.concat([smaSell, smaBuy, stochSell, stochBuy, rsiSell, rsiBuy],axis=1)
        sigTimeStamps.columns=['SMA Sell','SMA Buy','Stoch Sell','Stoch Buy','RSI Sell','RSI Buy']
        signals = sigTimeStamps.loc[sigTimeStamps['SMA Sell'] | sigTimeStamps['Stoch Sell'] |
                             sigTimeStamps['RSI Sell'] | sigTimeStamps['SMA Buy'] |
                             sigTimeStamps['Stoch Buy'] | sigTimeStamps['RSI Buy']]

        # Compare final signal Timestamp with latest data TimeStamp
        if (data.index[-1]==signals.index[-1]):
            final = signals.iloc[-1]
            # filter out the signals set to True and send to ChatBot
            signal = final.loc[final]
            signalTime = signal.name.strftime("%Y-%m-%dT%H:%M:%S")
            indicators = signal.loc[signal].index

            # Build the order
            order = [ticker,1,"buy","market","day"]
            try:
                gate.submit_order(order)
                print("Market " + order[2] + " order of " + str(order[1]) + " " + order[0] + " shares | completed")
            except:
                print("Market " + order[2] + " order of " + str(order[1]) + " " + order[0] + " shares | failed")
                # traceback.print_exc()
            # sendSignaltoChatBot(myRIC, signalTime, indicators)

    class MyFormatter(Formatter):
        def __init__(self, dates, fmt='%Y-%m-%d'):
            self.dates = dates
            self.fmt = fmt
        def __call__(self, x, pos=0):
            'Return the label for time x at position pos'
            ind = int(round(x))
            if ind>=len(self.dates) or ind<0: return ''
            return self.dates[ind].strftime(self.fmt)

    # Plot the Close price and short and long Simple Moving Averages
    def plotSMAs(self,ticker,close,sma14,sma200,sell,buy):
        x = close.index
        plt.rcParams["figure.figsize"] = (28,8)
        formatter = self.MyFormatter(x)
        fig, ax = plt.subplots(facecolor='0.25')
        ax.xaxis.set_major_formatter(formatter)
        ax.plot(np.arange(len(x)),close, label='Close',color='y')
        ax.plot(np.arange(len(x)),sma14,label="SMA 14", color='g')
        ax.plot(np.arange(len(x)),sma200,label="SMA 200", color='tab:purple')
        ax.tick_params(axis='both', colors='w')
        ax.set_facecolor('0.25')
        fig.autofmt_xdate()
        plt.ylabel('Close',color='y')
        plt.legend(loc='upper center',fontsize='x-large')
        plt.title(f"Simple Moving Average : {ticker}",color='w')
        plt.show()

    # Plot the Close price in the top chart and RSI in the lower chart
    def plotRSI(self,ticker,close,rsi):
        plt.rcParams["figure.figsize"] = (28,12)
        formatter = self.MyFormatter(rsi.index)
        fig = plt.figure(facecolor='0.25')
        gs1 = gridspec.GridSpec(2, 1)
        # RSI chart
        ax = fig.add_subplot(gs1[1])
        ax.xaxis.set_major_formatter(formatter)
        ax.plot(np.arange(len(rsi.index)), rsi.values,color='b')
        ax.tick_params(axis='both', colors='w')
        ax.set_ylabel('RSI', color='b')
        ax.set_facecolor('0.25')
        plt.axhline(y=70, color='w',linestyle='--')
        plt.axhline(y=30, color='w',linestyle='--')
        # Close Price chart
        axc = fig.add_subplot(gs1[0])
        axc.xaxis.set_major_formatter(formatter)
        axc.plot(np.arange(len(rsi.index)), close, color='y')
        axc.tick_params(axis='both', colors='w')
        axc.set_xticklabels([])
        axc.set_ylabel('Close', color='y')
        axc.set_facecolor('0.25')
        gs1.update(wspace=0.025, hspace=0.0)
        plt.title(f"Relative Strength : {ticker}",color='w')
        plt.show()

    # Plot Close price in top chart and in the slowk + slowd lines in lower chart
    def plotStoch(self,ticker,close,slowk,slowd):
        plt.rcParams["figure.figsize"] = (28,12)
        formatter = self.MyFormatter(slowk.index)
        fig = plt.figure(facecolor='0.25')
        gs1 = gridspec.GridSpec(2, 1)
        ax = fig.add_subplot(gs1[1])
        # Stochastic lines chart
        ax.xaxis.set_major_formatter(formatter)
        ax.plot(np.arange(len(slowk.index)), slowk.values,label="Slow K",color='m')
        ax.plot(np.arange(len(slowk.index)), slowd.values,label="Slow D",color='g')
        ax.tick_params(axis='both', colors='w')
        plt.legend(loc='upper center',fontsize='x-large')
        plt.axhline(y=80, color='w',linestyle='--')
        plt.axhline(y=20, color='w',linestyle='--')
        # Closing price chart
        axc = fig.add_subplot(gs1[0])
        axc.xaxis.set_major_formatter(formatter)
        axc.set_ylabel('Close', color='y')
        axc.set_xticklabels([])
        axc.plot(np.arange(len(close.index)), close, color='y')
        axc.tick_params(axis='both', colors='w')
        gs1.update(wspace=0.025, hspace=0.0)
        plt.title(f"Stochastic : {ticker}",color='w')
        ax.set_facecolor('0.25')
        axc.set_facecolor('0.25')
        plt.show()

    # Calculate Start and End time for our historical data request window
    def get_timeframe(self,interval):
        end = datetime.date.today()
        start = {
          'minute': lambda end: end - relativedelta(days=5),
          'hour': lambda end: end - relativedelta(months=2),
          'daily': lambda end: end - relativedelta(years=2),
          'weekly': lambda end: end - relativedelta(years=5),
          'monthly': lambda end: end - relativedelta(years=10),
        }[interval](end)
        return start.strftime("%Y-%m-%dT%H:%M:%S"),end.strftime("%Y-%m-%dT%H:%M:%S")

    # Await market open function
    def awaitMarketOpen(self):
      self.isOpen = self.gate.get_clock().is_open
      while(not self.isOpen):
        clock = self.gate.get_clock()
        openingTime = clock.next_open.replace(tzinfo=datetime.timezone.utc).timestamp()
        currTime = clock.timestamp.replace(tzinfo=datetime.timezone.utc).timestamp()
        timeToOpen = int((openingTime - currTime) / 60)
        # print("Current Time : " + str(datetime.today))
        print(str(timeToOpen) + " minutes til market open.")
        time.sleep(60)
        self.isOpen = self.gate.get_clock().is_open

    def run(self):
        interval = 'minute'    # 'minute', 'hour', 'daily', 'weekly', 'monthly'
        end = datetime.date.today()
        myStart, myEnd = self.get_timeframe(interval)
        # start = {
        #   'minute': lambda end: end - relativedelta(days=5),
        #   'hour': lambda end: end - relativedelta(months=2),
        #   'daily': lambda end: end - relativedelta(years=2),
        #   'weekly': lambda end: end - relativedelta(years=5),
        #   'monthly': lambda end: end - relativedelta(years=10),
        # }[interval](end)
        # myStart = start.strftime("%Y-%m-%dT%H:%M:%S")
        # myEnd = end.strftime("%Y-%m-%dT%H:%M:%S")
        limit = 800
        shortPeriod = 14
        longPeriod = 100
        basket={}
        # Do we want to plot charts?
        plotCharts = False
        # Dataframe display setting
        pd.set_option("display.max_rows", 999)
        pd.set_option('precision', 3)

        # Get historical data
        print('Running historical analysis...')
        for stock in self.stocks_to_trade:
            barset = pd.DataFrame(self.gate.get_barset(stock,
                start=myStart,
                end=myEnd,
                timeframe = interval,
                limit=limit).df)
            price = pd.Series(barset[stock]['close'])
            high = pd.Series(barset[stock]['high'])
            low = pd.Series(barset[stock]['low'])
            open = pd.Series(barset[stock]['open'])

            # keep
            basket[stock]=barset # Save each instrument's raw data for later use

            # Do the Simple Moving Average calcs
            smaSell,smaBuy,shortSMA,longSMA = self.SMA(price,shortPeriod,longPeriod)
            if plotCharts:
                self.plotSMAs(stock,price,shortSMA,longSMA,smaSell,smaBuy)

            # Do the RSI calcs
            rsiSell,rsiBuy,rsi = self.RSI(price,shortPeriod)
            if plotCharts:
                self.plotRSI(stock,price,rsi)

            # Stochastic calcs
            stochSell,stochBuy,slowk,slowd = self.Stoch(price, high, low)
            if plotCharts:
                self.plotStoch(stock,price,slowk,slowd)


        # While market is open, rerun every minute
        while True:

            # Figure out when market will close
            clock = self.gate.get_clock()
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
                for stock in self.stocks_to_trade:
                    historical = basket[stock]
                    latest = pd.DataFrame(self.gate.get_barset(stock,
                        start=myStart,
                        end=myEnd,
                        timeframe = interval,
                        limit=1).df)

                    # Delete earliest data point
                    historical.drop(historical.index[0])
                    # Append latest data point
                    historical = historical.append(latest)
                    runAllTA(stock, historical)
                    # Udpate basket with latest values
                    basket[stock] = historical

                    # Do the Simple Moving Average calcs
                    smaSell,smaBuy,shortSMA,longSMA = self.SMA(price,shortPeriod,longPeriod)
                    if plotCharts:
                        self.plotSMAs(stock,price,shortSMA,longSMA,smaSell,smaBuy)

                    # Do the RSI calcs
                    rsiSell,rsiBuy,rsi = self.RSI(price,shortPeriod)
                    if plotCharts:
                        self.plotRSI(stock,price,rsi)

                    # Stochastic calcs
                    stochSell,stochBuy,slowk,slowd = self.Stoch(price, high, low)
                    if plotCharts:
                        self.plotStoch(stock,price,slowk,slowd)

            # sleep for 60 seconds, then run again
            time.sleep(60)

if __name__ == '__main__':
    algobot = AlgoBot()
    algobot.run()

# EOF
