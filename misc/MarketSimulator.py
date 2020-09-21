# Market Simulator Class

# Class is used to fix market assumptions
    # indicate rejection rate
    # which type of orders can be accepted
    # set the trading rules belonging to the respective exchange

class MarketSimulator:
    def __init__(self, om_2_gw = None, gw_2_om = None):
        self.orders = []
        self.om_2_gw = om_2_gw
        self.gw_2_om = gw_2_om

    # Helps look up outstanding orders
    def lookup_orders(self, order):
        count = 0
        for o in self.orders:
            if o['id'] == order['id']:
                return o, count
            count += 1
            return None, None

    # Collect the order from the gateway (the order manager) through the om_2_gw channel
    def handle_order_from_gw(self):
        if sel.om_2_gw is not None:
            if len(self.om_2_gw) > 0:
                self.handle_order(self.om_2_gw.popleft())
            else:
                print('simulation mode')

    # Trading rules
        # function will accept any new orders
        # if an order ID already exists, the order will be dropped
        # if the order manager cancels or amends and order, the order is automatically deleted or amended
    def handle_order(self, order):
        o, offset = self.lookup_orders(order)
        if o is None:
            if order['action'] == 'new':
                order['status'] = 'accepted'
                self.orders.append(order)
                if self.gw_2_om is not None:
                    self.gw_2_om.append(order.copy())
                else:
                    print('simulation mode')
                return
            elif order['action'] == 'cancel' or order['action'] == 'amend':
                print('Order id - not found - Rejection')
                if self.gw_2_om is not None:
                    self.gw_2_om.append(order.copy())
                else:
                    print('simulation mode')
                return
        elif o is not None:
            if order['action'] == 'new':
                print('Duplicate order id - Rejection')
                return
            elif order['action'] == 'cancel':
                o['status'] == 'cancelled'
                if self.gw_2_om is not None:
                    self.gw_2_om.append(o.copy())
                else:
                    print('simulation mode')
                del (self.orders[offset])
                print('Order cancelled')
            elif order['action'] == 'amend':
                o['status'] = 'accepted'
                if self.gw_2_om is not None:
                    self.gw_2_om.append(o.copy())
                else:
                    print('simulation mode')
                print('Order amended')

    def fill_all_orders(self):
        orders_to_be_removed = []
        for index, order in enumerate(self.orders):
            order['status'] = 'filled'
            orders_to_be_removed.append(index)
            if self.gw_2_om is not None:
                self.gw_2_om.append(order.copy())
            else:
                print('simulation mode')
        for i in sorted(orders_to_be_removed, reverse = True):
            del (self.orders[i])

# EOF
