import bisect
import configparser
import sys
import time
from collections import defaultdict

from alpha_vantage.timeseries import TimeSeries
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from finance_tables import DailyQuote

conf = configparser.ConfigParser()

conf.read(sys.argv[1])
connection = conf['connection']
engine = create_engine("mysql+mysqldb://%s:%s@%s:%s/%s" % (
    connection['username'],
    connection['password'],
    connection['server_host'],
    connection['port'],
    connection['database']
))

conf.read(sys.argv[2])
alpha_vantage_key = conf['alpha_vantage']['key']

Session = sessionmaker(bind=engine)

if __name__ == '__main__':
  session = Session()
  ts = TimeSeries(key=alpha_vantage_key, output_format='json')

  with engine.connect() as con:
    with open('./sql/missing_dates.sql', 'r') as fd:
      result = con.execute(fd.read())
      missing_dates = defaultdict(lambda: set())
      for data in result.fetchall():
        missing_dates[data[0]].add(data[1])
      for symbol in missing_dates.keys():
        quotes = ts.get_daily(symbol=symbol, outputsize='full')[0]
        sorted_dates = sorted(quotes)
        for d in missing_dates[symbol]:
          idx = bisect.bisect_left(sorted_dates, str(d))
          previous_close = quotes[sorted_dates[idx - 1]]['4. close']
          quote = quotes[sorted_dates[idx]]
          session.merge(DailyQuote(
              symbol=symbol,
              date=d,
              open=quote['1. open'],
              high=quote['2. high'],
              low=quote['3. low'],
              close=quote['4. close'],
              volume=quote['5. volume'],
              previous_close=previous_close))
        time.sleep(15)
  session.commit()
  session.close()
