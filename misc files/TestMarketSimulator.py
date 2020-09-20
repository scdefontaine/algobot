# TestMarketSimulator Class

import unittest
from LiquidityProvider import LiquidityProvider
from TradingStrategy import TradingStrategy
# from MarketSimulator import MarketSimulator

class TestMarketSimulator(unittest.TestCase):
    def setUp(self):
        self.liquidity_provider = LiquidityProvider()
        self.trading_strategy = TradingStrategy()
        # self.market_simulator = MarketSimulator()

    # ***********************
    # TEST LIQUIDITY PROVIDER
    # ***********************

    # def test_add_liquidity(self):
    #     # Test the generate_random_order function and compare generated values to expected values
    #     self.liquidity_provider.generate_random_order()
    #     self.assertEqual(self.liquidity_provider.orders[0]['id'],0)
    #     self.assertEqual(self.liquidity_provider.orders[0]['side'],'buy')
    #     self.assertEqual(self.liquidity_provider.orders[0]['quantity'],700)
    #     self.assertEqual(self.liquidity_provider.orders[0]['price'], 11)
    #     print('Success')

    # ***********************
    # TEST TRADING STRATEGY
    # ***********************

    # Validate that the book event sent by the book is received correctly
    def test_receive_top_of_book(self):
        book_event = {
            "bid_price": 12,
            "bid_quantity" : 100,
            "offer_price" : 11,
            "offer_quantity" : 150
        }

        self.trading_strategy.handle_book_event(book_event)
        self.assertEqual(len(self.trading_strategy.orders), 2)
        self.assertEqual(self.trading_strategy.orders[0]['side'], 'sell')
        self.assertEqual(self.trading_strategy.orders[1]['side'], 'buy')
        self.assertEqual(self.trading_strategy.orders[0]['price'], 12)
        self.assertEqual(self.trading_strategy.orders[1]['price'], 11)
        self.assertEqual(self.trading_strategy.orders[0]['quantity'], 100)
        self.assertEqual(self.trading_strategy.orders[1]['quantity'], 100)
        self.assertEqual(self.trading_strategy.orders[0]['action'], 'no_action')
        self.assertEqual(self.trading_strategy.orders[1]['action'], 'no_action')

    # Verify whether the trading strategy receives the market response coming from the order manager
    # and whether is deletes the order created
    def test_rejected_order(self):
        self.test_receive_top_of_book()
        order_execution = {
            'id': 1,
            'price': 12,
            'quantity': 100,
            'side': 'sell',
            'status': 'rejected'
        }
        self.trading_strategy.handle_market_response(order_execution)
        self.assertEqual(self.trading_strategy.orders[0]['side'], 'buy')
        self.assertEqual(self.trading_strategy.orders[0]['price'], 11)
        self.assertEqual(self.trading_strategy.orders[0]['quantity'], 100)
        self.assertEqual(self.trading_strategy.orders[0]['status'], 'new')

    # Test the behavior of the trading strategy when the order is filled
    def test_filled_order(self):
        self.test_receive_top_of_book()
        order_execution = {
            'id': 1,
            'price': 11,
            'quantity': 100,
            'side': 'sell',
            'status': 'filled'
        }
        self.trading_strategy.handle_market_response(order_execution)
        self.assertEqual(len(self.trading_strategy.orders),1)

        order_execution = {
            'id': 2,
            'price': 12,
            'quantity': 100,
            'side': 'buy',
            'status': 'filled'
        }
        self.trading_strategy.handle_market_response(order_execution)
        self.assertEqual(self.trading_strategy.position,0)
        self.assertEqual(self.trading_strategy.cash,10000)
        self.assertEqual(self.trading_strategy.pnl, 100)

    # ***********************
    # TEST MARKET SIMULATOR
    # ***********************

    # Ensure all trading rules are verified
    # def test_accept_order(self):
    #     self.market_simulator
    #     order1 = {
    #         'id': 10,
    #         'price': 219,
    #         'quantity': 10,
    #         'side': 'bid',
    #         'action': 'new'
    #     }
    #     self.market_simulator.handle_order(order1)
    #     self.assertEqual(len(self.market_simulator.orders),1)
    #     self.assertEqual(self.market_simulator.orders[0]['status'], 'accepted')
    #
    # def test_accept_order(self):
    #     self.market_simulator
    #     order1 = {
    #         'id': 10,
    #         'price': 219,
    #         'quantity': 10,
    #         'side': 'bid',
    #         'action': 'amend'
    #     }
    #     self.market_simulator.handle_order(order1)
    #     self.assertEqual(len(self.market_simulator.orders),0)

if __name__ == '__main__':
    unittest.main()

# EOF
