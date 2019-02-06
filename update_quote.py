import datetime
import time

from sqlalchemy import Column, TIMESTAMP, CHAR, Date, DECIMAL, create_engine, \
  ForeignKey, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from alpha_vantage.timeseries import TimeSeries

engine = create_engine('mysql+mysqldb://root:eboue@localhost/finance')

Base = declarative_base()

Session = sessionmaker(bind=engine)


class SecurityType(Base):
  __tablename__ = 'SecurityTypes'

  type_id = Column('TypeId', CHAR(30), nullable=False, primary_key=True)
  description = Column('Description', CHAR(120))
  creation_timestamp = Column('CreationTimestamp', TIMESTAMP, nullable=False,
                              default=datetime.datetime.now)


class Security(Base):
  __tablename__ = 'Securities'

  symbol = Column('Symbol', CHAR(10), nullable=False, primary_key=True)
  description = Column('Description', CHAR(120))
  exchange = Column('Exchange', CHAR(20), nullable=False)
  type_id = Column('TypeId', CHAR(30), ForeignKey('SecurityTypes.TypeId',
                                                  name='Securities_TypeIdFK'),
                   nullable=False)
  creation_timestamp = Column('CreationTimestamp', TIMESTAMP, nullable=False,
                              default=datetime.datetime.now)


class DailyQuote(Base):
  __tablename__ = 'DailyQuote'

  symbol = Column('Symbol', CHAR(10), nullable=False, primary_key=True)
  date = Column('Date', Date, nullable=False, primary_key=True)
  open = Column('Open', DECIMAL(19, 6), nullable=False)
  high = Column('High', DECIMAL(19, 6), nullable=False)
  low = Column('Low', DECIMAL(19, 6), nullable=False)
  close = Column('Close', DECIMAL(19, 6), nullable=False)
  volume = Column('Volume', DECIMAL(19, 6), nullable=False)
  previous_close = Column('PreviousClose', DECIMAL(19, 6), nullable=False)
  currency = Column('Currency', CHAR(5), nullable=False, server_default='USD')
  creation_timestamp = Column('CreationTimestamp', TIMESTAMP, nullable=False,
                              default=datetime.datetime.now)
  Index('Date', date)


if __name__ == '__main__':
  session = Session()
  ts = TimeSeries(key='92FRTVHCC356S9ZS', output_format='json')
  for symbol in session.query(Security.symbol):
    resp = ts.get_quote_endpoint(symbol)[0]
    quote = DailyQuote(symbol=symbol,
                       date=resp['07. latest trading day'],
                       open=resp['02. open'],
                       high=resp['03. high'],
                       low=resp['04. low'],
                       close=resp['05. price'],
                       volume=resp['06. volume'],
                       previous_close=resp['08. previous close'])
    session.add(quote)
    session.commit()
    print(resp)
    time.sleep(15)
  session.close()