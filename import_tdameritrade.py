import configparser
import csv
import datetime
import re
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
      if 'dividend' in row['Description'].lower():
        symbol_match = re.search('~([A-Z]+)', row['Description'])
        if not symbol_match:
          symbol_match = re.search('\(([A-Z]+)\)', row['Description'])
        if symbol_match:
          dividend = Dividend(
              symbol=symbol_match.group(1),
              date=datetime.datetime.strptime(row['Date/Time'],
                                              '%m/%d/%Y %H:%M:%S'),
              account_id=2,
              amount=float(row['Amount'].strip('$').replace(',', '')))
          session.add(dividend)
      else:
        if row['Description'].startswith('Bought'):
          quantity_sign = 1
        elif row['Description'].startswith('Sold'):
          quantity_sign = -1
        else:
          continue
        transation_match = re.search('(\d+) ([A-Z]+) @ ([+-]?[\d,]+.?\d*)',
                                     row['Description'])
        transaction = Transactions(
            symbol=transation_match.group(2),
            date=datetime.datetime.strptime(row['Date/Time'],
                                            '%m/%d/%Y %H:%M:%S'),
            account_id=2,
            type_id=row['Type'],
            quantity=quantity_sign * float(transation_match.group(1)),
            price=float(transation_match.group(3).replace(',', ''))
        )
        session.add(transaction)
  session.commit()
  session.close()
