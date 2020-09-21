# Market Gateway Class
    # Connects to trading exchanges
    # Hanldes api protocol translation into class variables
        # FIX & HTTP


import sys
import time
import traceback
import alpaca_trade_api as tradeapi
from kiteconnect import KiteConnect

class MarketGateway:

    def __init__(self):

        # get credentials from external txt file

        # alpaca paper trading
        alpaca_url = "https://paper-api.alpaca.markets"
        alpaca_key = "PKMCXT8TUQH0YR06LFN7"
        alpaca_secret = "euc5bT52sNStFI4PDKg8hrQvrZxF/MeLQak6WEhi"
        self.alpaca = tradeapi.REST(alpaca_key,alpaca_secret,alpaca_url,'v2')

        # kite connect
        # kite_key = "u3gskacuz9pqc3rw"
        # self.kite = KiteConnect(api_key=kite_key)


    # ------------------------------------------------
    # Gateway OUT Functions - LIVE TRADING
    # ------------------------------------------------

    # --------- NORMAL BROKERAGE FUNCTIONS -----------

    def kite_account(self):
        return self.kite.profile()

    def orders(self):
        return self.kite.orders()

    def order_history(self, order_id):
        return self.kite.order_history(order_id)

    def positions(self):
        return self.kite.positions()

    def instruments(self, exchange=None):
        return self.kite.instruments(exchange)

    def quote(self, *instruments):
        return self.kite.quote(instruments)

    def ohlc_values(self, *instruments):
        return self.kite.ohlc(instruments)

    def last_price(self, *instruments):
        return self.kite.ltp(instruments)

    def historical_data(self, instrument_token, from_date, to_date, interval, continuous=False, oi=False):
        return self.kite.historical_data(self,instrument_token,from_date,to_date,interval,continuous,oi)


    # --------- SESSION & ACCESS TOKEN FUNCTIONS -----

    def generate_session(self, request_token, api_secret):
        return self.kite.generate_session(request_token)

    def renew_access_token(self, refresh_token, api_secret):
        return self.kite.renew_access_token(refresh_token,api_secret)

    def login_url(self):
        return self.kite.login_url()

    def renew_access_token(self, refresh_token, api_secret):
        return self.kite.renew_access_token(refresh_token, api_secret)


    # ------------------------------------------------
    # Gateway OUT Functions - LIVE TRADING
    # ------------------------------------------------

    def place_order(self,
                    variety,
                    exchange,
                    tradingsymbol,
                    transaction_type,
                    quantity,
                    product,
                    order_type,
                    price=None,
                    validity=None,
                    disclosed_quantity=None,
                    trigger_price=None,
                    squareoff=None,
                    stoploss=None,
                    trailing_stoploss=None,
                    tag=None):
        return self.kite.place_order(variety,
                                    exchange,
                                    tradingsymbol,
                                    transaction_type,
                                    quantity,
                                    product,
                                    order_type,
                                    price,
                                    validity,
                                    disclosed_quantity,
                                    trigger_price,
                                    squareoff,
                                    stoploss,
                                    trailing_stoploss,
                                    tag)

    def modify_order(self,
                     variety,
                     order_id,
                     parent_order_id=None,
                     quantity=None,
                     price=None,
                     order_type=None,
                     trigger_price=None,
                     validity=None,
                     disclosed_quantity=None):
        return self.kite.modify_order(variety,
                                     order_id,
                                     parent_order_id,
                                     quantity,
                                     price,
                                     order_type,
                                     trigger_price,
                                     validity,
                                     disclosed_quantity)

    def cancel_order(self, variety, order_id, parent_order_id=None):
        return self.kite.cancel_order(variety, order_id, parent_order_id)


    # -----------------------------------------------------------------

    # ------------------------------------------------
    # Gateway IN Functions - PAPER TRADING
    # ------------------------------------------------

    # get market data
    def get_market_data(self):
        return

    # get barset
    def get_barset(self,
                    symbols,
                    timeframe: str,
                    limit: int = None,
                    start: str = None,
                    end: str = None,
                    after: str = None,
                    until: str = None):
        return self.alpaca.get_barset(symbols,
                                        timeframe,
                                        limit,
                                        start,
                                        end,
                                        after,
                                        until)

    # Get the clock
    def get_clock(self):
        return self.alpaca.get_clock()

    # get account info
    def get_account(self):
        return self.alpaca.get_account()

    # List all orders
    def get_all_orders(self):
        return self.alpaca.list_orders()

    # Get a specific order via order_id
    def get_order(self, order):
        return self.alpaca.get_order(order[0])

    # List all Positions
    def get_all_positions(self):
        return self.alpaca.list_positions()

    # Get a specific position
    def get_position(self, symbol):
        return self.alpaca.get_position(symbol)

    # Get portfolio history
    def get_portfolio_history(self,start,end):
        return self.alpaca.get_portfolio_history(start,end)

    # ------------------------------------------------
    # Gateway OUT Functions - PAPER TRADING
    # ------------------------------------------------

    # Close a position via it's position_id
    def close_position(self, symbol):
        return self.alpaca.close_position(symbol)

    # close all positions
    def close_all_positions(self):
        return self.alpaca.close_all_positions()

    # modify an order
        # add additional params based on # of order keys
    def modify_order(self, order):
        return self.alpaca.replace_order(order[0])

    # cancel an order via it's order_id
    def cancel_order(self, order):
        return self.alpaca.cancel_order(order[0])

    # cancel all orders
    def cancel_all_orders(self):
        return self.alpaca.cancel_all_orders()

    # Submit order
    def submit_order(self, order):
        return self.alpaca.submit_order(order[0], order[1], order[2], order[3], order[4])

# EOF
