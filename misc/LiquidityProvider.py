# Liquidity Provider

from random import randrange
from random import sample, seed

# Goal of this class is to act as a liquidity provider or an exchange
class LiquidityProvider:
    def __init__(self, lp_2_gateway=None):
        self.orders = []
        self.order_id = 0
        seed(0)
        self.lp_2_gateway = lp_2_gateway


    # Utility function to look up orders in the list of orders
    def lookup_orders(self,id):
        count = 0
        for o in self.orders:
            if o['id'] == id:
                return o, count
            count += 1
        return None, None

    # This function inserts orders manually into the trading system
        # Used for unit testing some components
    def insert_manual_order(self, order):
        if self.lp_2_gateway is None:
            print('simulation mode')
            return order
        self.lp_2_gateway.append(order.copy())

    # Randomly generates 3 types of orders
        # New - creates a new order ID
        # Modify - uses the order id to make changes
        # Delete - uses the order id to delete an order
    def generate_random_order(self):
        price = randrange(8,12)
        qty = randrange(1,10)*100
        side = sample(['buy','sell'],1)[0]
        order_id = randrange(0,self.order_id + 1)
        o = self.lookup_orders(order_id)

        new_order = False
        if o is None:
            action = 'new'
            new_order = True
        else:
            action = sample(['modify','delete'],1)[0]

        ord = {
            'id': self.order_id,
            'price': price,
            'quantity': qty,
            'side': side,
            'action': action
        }

        if not new_order:
            self.order_id += 1
            self.orders.append(ord)

        if not self.lp_2_gateway:
            print('simulation mode')
            return ord
        self.lp_2_gateway.append(ord.copy())
