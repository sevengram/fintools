import configparser
import csv
import datetime
import sys

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from finance_tables import Dividend
from finance_tables import Transactions

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

if __name__ == '__main__':
  session = Session()
  with open(sys.argv[1]) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      if row['Action'] == 'Cash Dividend':
        dividend = Dividend(
            symbol=row['Symbol'],
            date=datetime.datetime.strptime(row['Date'], '%m/%d/%Y'),
            account_id=int(row['Account']),
            amount=float(row['Amount'].strip('$').replace(',', '')))
        session.add(dividend)
      else:
        if row['Action'] == 'Buy':
          quantity_sign = 1
        elif row['Action'] == 'Sell':
          quantity_sign = -1
        else:
          continue
        transaction = Transactions(
            symbol=row['Symbol'],
            date=datetime.datetime.strptime(row['Date'], '%m/%d/%Y'),
            account_id=int(row['Account']),
            type_id=row['Type'],
            quantity=quantity_sign * float(row['Quantity']),
            price=float(row['Price'].strip('$').replace(',', ''))
        )
        session.add(transaction)
  session.commit()
  session.close()
