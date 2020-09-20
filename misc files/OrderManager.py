# Order Manager Class

# Gather the orders from all the trading strategies and communicate
# this order with the market. It will check the validity of the orders
# and also keep track of the overall positions and PnL

class OrderManager:
    def __init__(self, ts_2_om = None, om_2_ts = None,
                om_2_gw = None, gw_2_om = None):
        self.orders = []
        self.order_id = 0
        self.ts_2_om = ts_2_om
        self.om_2_ts = om_2_ts
        self.gw_2_om = gw_2_om
        self.om_2_gw = om_2_gw

    # Check whether the ts_2_om channel has been created
        # if channel has not been created, use the class for unit testing only
        # to get new orders into OrderManager, check whether the size of the ts_2_om channel is higher than 0
        # if there is an order in the channel, remove this order and call handle_order_from_trading_strategy()
    def handle_input_from_ts(self):
        if self.ts_2_om is not None:
            if len(self.ts_2_om) > 0:
                self.handle_order_from_trading_strategy(self.ts_2_om.popleft())
        else:
            print('simulation mode')

    # Handles the new order coming from the traidng strategies
    def handle_order_from_trading_strategy(self, order):
        if self.check_order_valid(order):
            order = self.create_new_order(order).copy()
            self.orders.append(order)
            if self.om_2_gw is None:
                print('simulation mode')
            else:
                self.om_2_gw.append(order.copy())

    # Checks whether the gw_2_om channel exists
        # if so, the functions reads the market response object coming from the market and calls the handle_order_from_gateway
    def handle_input_from_market(self):
        if self.gw_2_om is not None:
            if len(self.gw_2_om) > 0:
                self.handle_order_from_gateway(self.gw_2_om.popleft())
        else:
            print('simulation mode')

    # look up the list of orders created by handle_order_from_trading_strategy
    def handle_order_from_gateway(self, order_update):
        order = self.lookup_order_by_id(order_update['id'])
        if order is not None:
            order['status'] = order_update['status']
            if self.om_2_ts is not None:
                self.om_2_ts.append(order.copy())
            else:
                print('simulation mode')
            self.clean_traded_orders()
        else:
            print('order not found')

    # Checks on an order
    def check_order_valid(self, order):
        if order['quantity'] < 0:
            return False
        if order['price'] < 0:
            return False
        return True

    # Creates a dictionary to store the order characteristics
    def create_new_order(self, order):
        self.order_id += 1
        new_order = {
            'id': self.order_id,
            'price': order['price'],
            'quantity': order['quantity'],
            'side': order['side'],
            'status': 'new',
            'action': 'new'
        }
        return new_order

    # Returns a reference to the order by looking up by order ID
    def lookup_order_by_id(self, id):
        for i in range(len(self.orders)):
            if self.orders[i]['id'] == id:
                return self.orders[i]
        return None

    # Removes all the orders that have been filled from the list of orders
    def clean_traded_orders(self):
        order_offsets = []
        for k in range(len(self.orders)):
            if self.orders[k]['status'] == 'filled':
                order_offsets.append(k)
        if len(order_offsets):
            for k in sorted(order_offsets, reverse = True):
                del (self.orders[k])


# EOF
