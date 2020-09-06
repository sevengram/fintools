import configparser
import csv
import sys

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from finance_tables import Industry
from finance_tables import SecuritySector

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
  sector_map = {description: sector_id for sector_id, description in
                session.query(Industry.sector_id, Industry.description)}
  with open(sys.argv[1]) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      security_sector = SecuritySector(
          symbol=row['Symbol'],
          sector_id=sector_map[row['Sector']],
          weight=float(row['Weight']))
      session.add(security_sector)
  session.commit()
  session.close()
