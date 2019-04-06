import csv
import sys
import datetime

import configparser
from sqlalchemy import create_engine, Column, TIMESTAMP, CHAR, Integer, DATE, \
  DECIMAL, ForeignKey, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

conf = configparser.ConfigParser()

conf.read(sys.argv[2])
connection = conf['connection']
engine = create_engine("mysql+mysqldb://%s:%s@%s:%s/%s" % (
  connection['username'],
  connection['password'],
  connection['server_host'],
  connection['port'],
  connection['database']
))

Base = declarative_base()

Session = sessionmaker(bind=engine)


class Accounts(Base):
  __tablename__ = 'Accounts'

  account_id = Column('AccountId', Integer, nullable=False, primary_key=True)
  brokerage = Column('Brokerage', CHAR(20), nullable=False)
  account_number = Column('AccountNumber', CHAR(30))
  description = Column('Description', CHAR(120))
  creation_timestamp = Column('CreationTimestamp', TIMESTAMP, nullable=False,
                              default=datetime.datetime.now)


class Dividends(Base):
  __tablename__ = 'Dividends'

  type_id = Column('DividendId', Integer, nullable=False, primary_key=True)
  symbol = Column('Symbol', CHAR(10), nullable=False)
  date = Column('Date', DATE, nullable=False)
  accountId = Column(
      'AccountId',
      Integer,
      ForeignKey(Accounts.account_id, name='Dividends_AccountId_FK'),
      nullable=False)
  amount = Column('Amount', DECIMAL(13, 4), nullable=False)
  currency = Column('Currency', CHAR(5), nullable=False, server_default='USD')
  creation_timestamp = Column(
      'CreationTimestamp',
      TIMESTAMP,
      nullable=False,
      default=datetime.datetime.now)

  Index('Dividends_Symbol_IDX', symbol)
  Index('Dividends_Date_IDX', date)


if __name__ == '__main__':
  session = Session()
  with open(sys.argv[1]) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      dividend = Dividends(
          symbol=row['Symbol'],
          date=datetime.datetime.strptime(row['Date'], '%m/%d/%Y'),
          accountId=2,
          amount=float(row['Amount'].replace('$', '')))
      session.add(dividend)
  session.commit()
  session.close()
