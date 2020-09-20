# TestOrderManager class
import unittest
from OrderManager import OrderManager

class TestOrderManager(unittest.TestCase):
    def setUp(self):
        self.order_manager = OrderManager()

    # Verify whether an order is correctly received by the order Manager
    def test_receive_order_from_trading_strategy(self):
        order1 = {
            'id': 10,
            'price': 219,
            'quantity': 10,
            'side': 'bid'
        }
        self.order_manager.handle_order_from_trading_strategy(order1)
        self.assertEqual(len(self.order_manager.orders),1)
        self.order_manager.handle_order_from_trading_strategy(order1)
        self.assertEqual(len(self.order_manager.orders),2)
        self.assertEqual(self.order_manager.orders[0]['id'],1)
        self.assertEqual(self.order_manager.orders[1]['id'],2)

    # Checks whether an order created with a negative price is rejected
        # This prvents a malformed order from being sent to the market
    def test_receive_order_from_trading_strategy_error(self):
        order1 = {
            'id': 10,
            'price': -219,
            'quantity': 10,
            'side': 'bid'
        }
        self.order_manager.handle_order_from_trading_strategy(order1)
        self.assertEqual(len(self.order_manager.orders),0)

    # Confirm the market response has been propagated by the order manager
    def test_receive_from_gateway_filled(self):
        self.test_receive_order_from_trading_strategy()
        order_execution_1 = {
            'id': 2,
            'price': 13,
            'quantity': 10,
            'side': 'bid',
            'status': 'filled'
        }
        self.order_manager.handle_order_from_gateway(order_execution_1)
        self.assertEqual(len(self.order_manager.orders), 1)

    def test_receive_from_gateway_acked(self):
        self.test_receive_order_from_trading_strategy()
        order_execution_1 = {
            'id': 2,
            'price': 13,
            'quantity': 10,
            'side': 'bid',
            'status': 'acked'
        }
        self.order_manager.handle_order_from_gateway(order_execution_1)
        self.assertEqual(len(self.order_manager.orders),2)
        self.assertEqual(self.order_manager.orders[1]['status'], 'acked')

# EOF
