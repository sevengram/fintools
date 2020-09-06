import configparser
import csv
import datetime
import sys

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from finance_tables import Dividend

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
      dividend = Dividend(
          symbol=row['Symbol'],
          date=datetime.datetime.strptime(row['Date'], '%m/%d/%Y'),
          account_id=2,
          amount=float(row['Amount'].replace('$', '')))
      session.add(dividend)
  session.commit()
  session.close()
