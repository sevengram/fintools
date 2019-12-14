import bisect
import configparser
import sys

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
  result = ts.get_daily(symbol='SPY', outputsize='full')[0]

  previous_close = result['2018-09-14']['4. close']
  sorted_dates = sorted(result)
  for key in sorted_dates[bisect.bisect_right(sorted_dates, '2018-09-14'):]:
    quote = result[key]
    session.merge(DailyQuote(
        symbol='SPY',
        date=key,
        open=quote['1. open'],
        high=quote['2. high'],
        low=quote['3. low'],
        close=quote['4. close'],
        volume=quote['5. volume'],
        previous_close=previous_close))
    previous_close = quote['4. close']
  session.commit()
  session.close()
