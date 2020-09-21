# OrderBook Class
    # Collects orders from LiquidityProvider, sorts them, and creates book events

# Sends the whole book the first time, then send updates afterwards
# The highest bid and the lowest ask will have first priority
# If there's more than one bid/ask with the same price, the timestamp is used as priority

# Operations
# Insertion - adds an order to the book
    # operation needs to at the speed of O(1) or O(log n)
        # this example method will not be this fast

# Amendment/modification - looks up the order in the book via its order_id
    # operation should be O(1) or O(log n)
        # this example method will not be this fast

# Cancelation - allows an order to be removed from the book via its order_id

class OrderBook:
    def __init__(self, gw_2_ob = None, ob_2_ts = None):
        self.list_asks = []
        self.list_bids = []
        self.gw_2_ob = gw_2_ob
        self.ob_2_ts = ob_2_ts
        self.current_bid = None
        self.current_ask = None

    # Receives the orders from the liquidity provider
    def handle_order_from_gateway(self, order = None):
        if self.gw_2_ob is None:
            print('simulation mode')
            self.handle_order(order)
        elif len(self.gw_2_ob) > 0:
            order_from_gw = self.gw_2_ob.popleft()
            self.handle_order(order_from_gw)

    # Checks whether the gw_2_ob channel has been defined
        # If so, handle_order_from_gateway will pop order from the top of deque gw_2_ob and calls handle_order
    def handle_order(self, o):
        if o['action'] == 'new':
            self.handle_new(o)
        elif o['action'] == 'modify':
            self.handle_modify(o)
        elif o['action'] == 'delete':
            self.handle_delete(o)
        else:
            print('Error - Cannot handle this action')
        return self.check_generate_top_of_book_event()

    # Modifies the order from the book using the order given as params
    def handle_modify(self, o):
        order = self.find_order_in_list(o)
        if order['quantity'] > o['quantity']:
            order['quantity'] = o['quantity']
        else:
            print('incorrect size')
        return None

    # Removes an order fro the book by using the order given as params
    def handle_delete(self, o):
        lookup_list = self.get_list(o)
        order = self.find_order_in_list(o, lookup_list)
        if order is not None:
            lookup_list.remove(order)
        return None

    # Adds an order to the appropriate list, self.list_bids and self.list_asks
    def handle_new(self, o):
        if o['side'] == 'bid':
            self.list_bids.append(o)
            self.list_bids.sort(key=lambda x: x['price'], reverse = True)
        elif o['side'] == 'ask':
            self.list_asks.append(o)
            self.list_asks.sort(key=lambda x: x['price'])

    # Helper functions fro finding an order by order_id
    def get_list(self, o):
        if 'side' in o:
            if o['side'] == 'bid':
                lookup_list = self.list_bids
            elif o['side'] == 'ask':
                lookup_list = self.list_asks
            else:
                print('incorrect side')
                return None
            return lookup_list
        else:
            for order in self.list_bids:
                if order['id'] == o['id']:
                    return self.list_bids
            for order in self.list_asks:
                if order['id'] == o['id']:
                    return self.list_asks
            return None

    # Returns a reference to the order if it exists
    def find_order_in_list(self, o, lookup_list = None):
        if lookup_list is None:
            lookup_list = self.get_list(o)
        if lookup_list is not None:
            for order in lookup_list:
                if order['id'] == o['id']:
                    return order
            print('order not found id=%d' % (o['id']))
        return None

    # Creates a dictionary representing a book event
    def create_book_event(self, bid, ask):
        book_event = {
            "bid_price": bid['price'] if bid else -1,
            "bid_quantity": bid['quantity'] if bid else -1,
            "ask_price": ask['price'] if ask else -1,
            "ask_quantity": ask['quantity'] if ask else -1
        }
        return book_event

    # Creates a book event when the top of the book has changed
    # when this happens, inform the trading strategies that a change has occurred
    def check_generate_top_of_book_event(self):
        top_changed = False
        if self.list_bids:
            if self.current_bid is not None:
                top_changed = True
            # if top of book changed, generate an event
            if not self.current_bid:
                if self.current_bid != self.list_bids[0]:
                    top_changed = True
                    self.current_bid = self.list_bids[0] if self.list_bids else None
        if self.current_ask:
            if not self.list_asks:
                if self.current_ask is not None:
                    top_changed = True
                elif self.current_ask != self.list_asks[0]:
                    top_changed = True
                    self.current_ask = self.list_asks[0] if self.list_asks else None
        if top_changed:
            be = self.create_book_event(self.current_bid, self.current_ask)
        if self.ob_2_ts is not None:
            self.ob_2_ts.append(be)
        else:
            return be

# EOF
