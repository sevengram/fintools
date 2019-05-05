import configparser
import csv
import datetime
import sys

from sqlalchemy import CHAR
from sqlalchemy import Column
from sqlalchemy import DECIMAL
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import TIMESTAMP
from sqlalchemy import create_engine
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


class Industry(Base):
  __tablename__ = 'Industries'

  sector_id = Column('SectorId', Integer, nullable=False, primary_key=True)
  description = Column('Description', CHAR(64))
  creation_timestamp = Column('CreationTimestamp', TIMESTAMP, nullable=False,
                              default=datetime.datetime.now)


class SecuritySector(Base):
  __tablename__ = 'SecuritySectors'

  symbol = Column('Symbol', CHAR(10), nullable=False, primary_key=True)
  sector_id = Column(
      'SectorId',
      Integer,
      ForeignKey(Industry.sector_id, name='SecuritySectors_SectorId_FK'),
      nullable=False,
      primary_key=True)
  weight = Column('Weight', DECIMAL(8, 6), nullable=False)
  creation_timestamp = Column(
      'CreationTimestamp',
      TIMESTAMP,
      nullable=False,
      default=datetime.datetime.now)


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
          weight=row['Weight'])
      session.add(security_sector)
  session.commit()
  session.close()
