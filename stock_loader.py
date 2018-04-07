import MySQLdb
import pandas as pd


class StockLoader(object):
  """Load stock time series data from MySQL schemas.

  Attributes:
    mysql_connection: The connection to the MySQL database.
  """

  def __init__(self):
    """Inits StockLoader."""
    self.mysql_connection = MySQLdb.connect(host="localhost", user="root",
                                            passwd="eboue", db="finance",
                                            port=3306)

  def get_price_volume(self, symbol, start_date, end_date):
    """Gets price and volume time series data.

    Args:
      symbol: The symbol of the stock.
      start_date: The start date of the time series.
      end_date: The end date of the time series.
    """

    query_format = """
      SELECT 
        Symbol,
        Date,
        Open,
        High,
        Low,
        Close,
        AdjOpen,
        AdjHigh,
        AdjLow,
        AdjClose,
        AdjVolume AS Volume,
        ExDividend > 1e-6 OR ABS(SplitRatio - 1.0) > 1e-6 AS HasEvent
      FROM StockPriceVolume 
      WHERE Symbol='%s' AND Date BETWEEN '%s' AND '%s' 
      ORDER BY Date"""
    query = query_format % (symbol.upper(), start_date, end_date)
    return pd.read_sql(query, con=self.mysql_connection)
