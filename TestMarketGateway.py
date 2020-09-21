# Test file for MarketGateway class

from MarketGateway import MarketGateway

class TestMarketGateway:
    def __init__(self):
        self.gw = MarketGateway()

    def test_get_barset(self, var):
        print(var)


    def test_get_request_token(self):
        print(self.gw.generate_access_token())








if __name__ == '__main__':
    test = TestMarketGateway()
    test.test_get_request_token()

# EOF
