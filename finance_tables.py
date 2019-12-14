import datetime

from sqlalchemy import CHAR
from sqlalchemy import Column
from sqlalchemy import DATE
from sqlalchemy import DECIMAL
from sqlalchemy import ForeignKey
from sqlalchemy import Index
from sqlalchemy import TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


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
  type_id = Column(
      'TypeId',
      CHAR(30),
      ForeignKey(SecurityType.type_id, name='Securities_SecurityTypes_FK'),
      nullable=False)
  creation_timestamp = Column(
      'CreationTimestamp',
      TIMESTAMP,
      nullable=False,
      default=datetime.datetime.now)


class DailyQuote(Base):
  __tablename__ = 'DailyQuote'

  symbol = Column('Symbol', CHAR(10), nullable=False, primary_key=True)
  date = Column('Date', DATE, nullable=False, primary_key=True)
  open = Column('Open', DECIMAL(19, 6), nullable=False)
  high = Column('High', DECIMAL(19, 6), nullable=False)
  low = Column('Low', DECIMAL(19, 6), nullable=False)
  close = Column('Close', DECIMAL(19, 6), nullable=False)
  volume = Column('Volume', DECIMAL(19, 6), nullable=False)
  previous_close = Column('PreviousClose', DECIMAL(19, 6), nullable=False)
  currency = Column('Currency', CHAR(5), nullable=False, server_default='USD')
  creation_timestamp = Column(
      'CreationTimestamp',
      TIMESTAMP,
      nullable=False,
      default=datetime.datetime.now)
  Index('DailyQuote_Date_IDX', date)
