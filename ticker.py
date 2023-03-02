from pykrx import stock
from pykrx import bond

class Ticker:

    def get_tiker(self):
        ticker_kospi = stock.get_market_ticker_list(market="KOSPI")
        ticker_kosdaq = stock.get_market_ticker_list(market="KOSDAQ")
        ticker = ticker_kosdaq+ticker_kospi

        return ticker

    def name_from_ticker(self, ticker_list):
        name_list=[]
        for ticker in ticker_list:
            name = stock.get_market_ticker_name(ticker)
            name_list.append(name)
        return name_list

    # ticker_list = get_tiker()
    # name_list = name_from_ticker(ticker_list=ticker_list)
