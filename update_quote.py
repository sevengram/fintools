import configparser
import sys
import time

from alpha_vantage.timeseries import TimeSeries
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from finance_tables import DailyQuote
from finance_tables import Security

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
  for symbol in session.query(Security.symbol):
    resp = ts.get_quote_endpoint(symbol)[0]
    print(resp)
    quote = DailyQuote(
        symbol=symbol,
        date=resp['07. latest trading day'],
        open=resp['02. open'],
        high=resp['03. high'],
        low=resp['04. low'],
        close=resp['05. price'],
        volume=resp['06. volume'],
        previous_close=resp['08. previous close'])
    session.merge(quote)
    time.sleep(15)
  session.commit()
  session.close()
