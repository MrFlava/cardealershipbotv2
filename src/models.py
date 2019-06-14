import os
import datetime
from botmanlib.models import db
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, String, Integer, DateTime, Boolean, ForeignKey

if not os.getenv('sqlalchemy.url'):
    from src.settings import PROJECT_ROOT
    import configparser
    config = configparser.ConfigParser()
    config.read(os.path.join(PROJECT_ROOT, 'botmanlib.ini'))
    os.environ['sqlalchemy.url'] = config['botmanlib']['sqlalchemy.url']

Base = db.Base
engine = create_engine(db.database_url)


class Cars(Base):

    __tablename__ = 'cars'

    id_car = Column(Integer, primary_key=True)
    car_type = Column(String)
    car_model = Column(String)
    description = Column(String)
    price = Column(Integer)

class User(Base):

    __tablename__ = 'users'

    id_user = Column(Integer, primary_key=True)
    chat_id = Column(Integer)
    name = Column(String)
    username = Column(String)
    active = Column(Boolean, default=True)
    join_date = Column(DateTime, default=datetime.datetime.now)

class Customers(Base):

    __tablename__ = 'customers_data'

    customer_id = Column(Integer, primary_key=True)
    customer_type = Column(String)
    phone = Column(Integer)
    ordered_car = Column(String)
    creating_date = Column(DateTime, default=datetime.datetime.now)

Session = sessionmaker(engine)
DBSession = Session()

