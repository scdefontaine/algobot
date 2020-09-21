# Strategy class



class Strategy:
    def __init__(self, gw, stocks_to_trade, trader):

        # api access
        self.gw = gw

        # External classes
        self.trader = trader

        # Class variables
        self.stocks_to_trade = stocks_to_trade
        self.orders = []    # order_id, symbol, qty, side, order_type, time_in_force

        #

    def get_rsi(self, close):
        return

    def run(self):
        # create thread to trading strategy class
        # Run Strategy
        print(" -------------------------------- ")
        timeframe = "minute"
        limit = 45
        for stock in self.stocks_to_trade:

            # get the ohlc values for each stock
            bars = pd.DataFrame(self.gw.get_barset(stock, timeframe, limit).df)
            self.ohlc_values = {
                "open": bars[stock]['open'][limit-1],
                "high": bars[stock]['high'][limit-1],
                "low": bars[stock]['low'][limit-1],
                "close": bars[stock]['close'][limit-1]
            }

            # get the close prices for each stock
            close_prices = bars[stock]['close']

            # Get the rsi values for each stock
            rsi_values = ta.momentum.RSIIndicator(pd.Series(data=close_prices))
            rsi = rsi_values.rsi()[limit - 1]    # use dropna for nan values

            # get trader buying power
            buying_power = self.trader.get_buying_power()

            if buying_power > 0:

                # check trading signal values
                if rsi < 30:
                    # how much to buy
                    qty = int(float(buying_power) / float(close_prices[limit-1]))
                    if qty > 1:
                        # send to order manager
                        # build the order
                        side = 'buy'
                        order = [ stock, qty, side, "market", "day" ]
                        # submit order to exchange
                        try:
                            self.gw.submit_order(order)
                            print("Market " + side + " order of " + str(qty) + " " + stock + " shares | completed")
                        except:
                            print("Market " + side + " order of " + str(qty) + " " + stock + " shares | failed")
                    else:
                        print("Not enough buying power")
                        self.gw.list_positions()
                elif rsi > 70:
                    # get positions & their quantity
                    print("RSI greater than 70. Selling positions")



























# EOF
