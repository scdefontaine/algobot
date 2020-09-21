# Trader Class




class Trader:

    def __init__(self, gw, id):

        # api access
        self.gw = gw

        self.trader_id = id
        self.is_dead = False

        # Account Info
        account = gw.get_account()
        self.portfolio_value = account.portfolio_value
        self.buying_power = account.buying_power
        # self.day_trade_count = 0
        self.positions = gw.get_all_positions()


    def set_portfolio_value(self, portfolio_value: int = None):
        self.portfolio_value = portfolio_value

    def get_portfolio_value(self):
        return self.portfolio_value

    def set_buying_power(self, buying_power: int = None):
        self.buying_power = buying_power

    def get_buying_power(self):
        return self.buying_power

    def set_positions(self, positions = None):
        self.positions = positions

    def get_positions(self):
        return self.positions

    def set_is_dead(self, is_dead):
        self.is_dead = is_dead

    def get_is_dead(self):
        return self.is_dead

    # Fitness is calculated based on the highest pnl percentage
    def calculate_fitness(self):
        fitness = self.gw.get_account().unrealized_pl





















# EOF
