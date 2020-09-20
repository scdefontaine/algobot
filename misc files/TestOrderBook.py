# Test Order Book Class
    # Adds a new order
    # Modifies a new order
    # Deletes an order
    # Creates a book event

import unittest
from OrderBook import OrderBook

class TestOrderBook(unittest.TestCase):
    def setUp(self):
        self.reforderbook = OrderBook()

    # Verify if the order insertion works
    # Book must have the the list of asks and the lists of bids sorted
    def test_handle_new(self):
        print(' test_handle_new ')
        # bids
        order1 = {
            'id': 1,
            'price': 219,
            'quantity': 10,
            'side': 'bid',
            'action': 'new'
        }
        ob_for_aapl = self.reforderbook
        ob_for_aapl.handle_order(order1)

        order2 = order1.copy()
        order2['id'] = 2
        order2['price'] = 220
        ob_for_aapl.handle_order(order2)

        order3 = order1.copy()
        order3['id'] = 3
        order3['price'] = 223
        ob_for_aapl.handle_order(order3)

        # asks
        order4 = {
            'id': 4,
            'price': 220,
            'quantity': 10,
            'side': 'ask',
            'action': 'new'
        }
        ob_for_aapl.handle_order(order4)

        order5 = order4.copy()
        order5['id'] = 5
        order5['price'] = 223
        ob_for_aapl.handle_order(order5)

        order6 = order4.copy()
        order6['id'] = 6
        order6['price'] = 221
        ob_for_aapl.handle_order(order6)

        self.assertEqual(ob_for_aapl.list_bids[0]['id'], 3)
        self.assertEqual(ob_for_aapl.list_bids[1]['id'], 2)
        self.assertEqual(ob_for_aapl.list_bids[2]['id'], 1)
        self.assertEqual(ob_for_aapl.list_asks[0]['id'], 4)
        self.assertEqual(ob_for_aapl.list_asks[1]['id'], 6)
        self.assertEqual(ob_for_aapl.list_asks[2]['id'], 5)

    # Test the amendment function by using test_handle_new and amend the order by changing the quantity
    def test_handle_amend(self):
        print(' test_handle_amend ')
        self.test_handle_new()
        order1 = {
            'id': 1,
            'quantity': 5,
            'action': 'modify'
        }
        self.reforderbook.handle_order(order1)

        self.assertEqual(self.reforderbook.list_bids[2]['id'], 1)
        self.assertEqual(self.reforderbook.list_bids[2]['quantity'], 5)

    # Test the removal of an order via order_id by filling the book with test_handle_new and removing the order
    def test_handle_delete(self):
        print(' test_handle_delete ')
        self.test_handle_new()
        order1 = {
            'id': 1,
            'action': 'delete'
        }
        self.assertEqual(len(self.reforderbook.list_bids), 3)
        self.reforderbook.handle_order(order1)
        self.assertEqual(len(self.reforderbook.list_bids), 2)

    # Test the creation of the book event after the top of the book changes
    def test_generate_book_event(self):
        print(' test_generate_book_event ')
        order1 = {
            'id': 1,
            'price': 219,
            'quantity': 10,
            'side': 'bid',
            'action': 'new'
        }
        ob_for_aapl = self.reforderbook
        self.assertEqual(ob_for_aapl.handle_order(order1),
                        {'bid_price': 219, 'bid_quantity': 10,
                        'ask_price': -1, 'ask_quantity': -1})

        order2 = order1.copy()
        order2['id'] = 2
        order2['price'] = 220
        order2['side'] = 'ask'
        self.assertEqual(ob_for_aapl.handle_order(order2),
                        {'bid_price': 219, 'bid_quantity': 10,
                        'ask_price': 220, 'ask_quantity': 10})

if __name__ == '__main__':
    unittest.main()


# EOF
