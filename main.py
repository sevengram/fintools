import datetime

from stock_loader import StockLoader

if __name__ == '__main__':
  loader = StockLoader()
  result = loader.get_price_volume('AAPL', datetime.date(2017, 1, 1),
                                   datetime.date(2017, 2, 1))
  print(result)