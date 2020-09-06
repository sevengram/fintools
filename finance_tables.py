import datetime

from sqlalchemy import CHAR
from sqlalchemy import Column
from sqlalchemy import DATE
from sqlalchemy import DECIMAL
from sqlalchemy import ForeignKey
from sqlalchemy import Index
from sqlalchemy import Integer
from sqlalchemy import TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class SecurityType(Base):
  __tablename__ = 'SecurityTypes'

  type_id = Column('TypeId', CHAR(30), primary_key=True)
  description = Column('Description', CHAR(120))
  creation_timestamp = Column('CreationTimestamp', TIMESTAMP,
                              default=datetime.datetime.now)


class Security(Base):
  __tablename__ = 'Securities'

  symbol = Column('Symbol', CHAR(10), primary_key=True)
  description = Column('Description', CHAR(120))
  exchange = Column('Exchange', CHAR(20))
  type_id = Column('TypeId', CHAR(30),
                   ForeignKey(SecurityType.type_id,
                              name='Securities_SecurityTypes_FK'))
  creation_timestamp = Column('CreationTimestamp', TIMESTAMP,
                              default=datetime.datetime.now)


class DailyQuote(Base):
  __tablename__ = 'DailyQuote'

  symbol = Column('Symbol', CHAR(10), primary_key=True)
  date = Column('Date', DATE, primary_key=True)
  open = Column('Open', DECIMAL(19, 6))
  high = Column('High', DECIMAL(19, 6))
  low = Column('Low', DECIMAL(19, 6), )
  close = Column('Close', DECIMAL(19, 6))
  volume = Column('Volume', DECIMAL(19, 6))
  previous_close = Column('PreviousClose', DECIMAL(19, 6))
  currency = Column('Currency', CHAR(5), server_default='USD')
  creation_timestamp = Column('CreationTimestamp', TIMESTAMP,
                              default=datetime.datetime.now)

  Index('DailyQuote_Date_IDX', date)


class Accounts(Base):
  __tablename__ = 'Accounts'

  account_id = Column('AccountId', Integer, primary_key=True)
  brokerage = Column('Brokerage', CHAR(20))
  account_number = Column('AccountNumber', CHAR(30))
  description = Column('Description', CHAR(120))
  creation_timestamp = Column('CreationTimestamp', TIMESTAMP,
                              default=datetime.datetime.now)


class Dividend(Base):
  __tablename__ = 'Dividends'

  dividend_id = Column('DividendId', Integer, primary_key=True)
  symbol = Column('Symbol', CHAR(10))
  date = Column('Date', DATE)
  account_id = Column('AccountId', Integer,
                      ForeignKey(Accounts.account_id,
                                 name='Dividends_AccountId_FK'))
  amount = Column('Amount', DECIMAL(13, 4))
  currency = Column('Currency', CHAR(5), server_default='USD')
  creation_timestamp = Column('CreationTimestamp', TIMESTAMP,
                              default=datetime.datetime.now)

  Index('Dividends_Symbol_IDX', symbol)
  Index('Dividends_Date_IDX', date)


class Industry(Base):
  __tablename__ = 'Industries'

  sector_id = Column('SectorId', Integer, primary_key=True)
  description = Column('Description', CHAR(64))
  creation_timestamp = Column('CreationTimestamp', TIMESTAMP,
                              default=datetime.datetime.now)


class SecuritySector(Base):
  __tablename__ = 'SecuritySectors'

  symbol = Column('Symbol', CHAR(10), primary_key=True)
  sector_id = Column('SectorId', Integer,
                     ForeignKey(Industry.sector_id,
                                name='SecuritySectors_SectorId_FK'),
                     primary_key=True)
  weight = Column('Weight', DECIMAL(8, 6), )
  creation_timestamp = Column('CreationTimestamp', TIMESTAMP,
                              default=datetime.datetime.now)


class Transactions(Base):
  __tablename__ = 'Transactions'

  transaction_id = Column('TransactionId', Integer, primary_key=True)
  symbol = Column('Symbol', CHAR(10))
  date = Column('Date', DATE)
  account_id = Column('AccountId', Integer,
                      ForeignKey(Accounts.account_id,
                                 name='Transactions_AccountId_FK'))
  type_id = Column('TypeId', CHAR(30))
  quantity = Column('Quantity', DECIMAL(13, 4))
  price = Column('Price', DECIMAL(13, 4))
  commission = Column('Commission', DECIMAL(13, 4), default=0)
  currency = Column('Currency', CHAR(5), server_default='USD')
  creation_timestamp = Column('CreationTimestamp', TIMESTAMP,
                              default=datetime.datetime.now)
