# Alpaca Bot


class AlgoBot:

    def __init__(self):

        file = open("sp500_tickers.txt", "r").read().split("\n")
        print(file)



if __name__ == '__main__':
    algobot = AlgoBot()

# EOF
