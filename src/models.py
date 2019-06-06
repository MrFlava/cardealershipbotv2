import os
import datetime
from botmanlib.models import db
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy import create_engine, Column, String, Integer, DateTime, Boolean, ForeignKey

if not os.getenv('sqlalchemy.url'):
    from src.settings import PROJECT_ROOT
    import configparser
    config = configparser.ConfigParser()
    config.read(os.path.join(PROJECT_ROOT, 'botmanlib.ini'))
    os.environ['sqlalchemy.url'] = config['botmanlib']['sqlalchemy.url']

Base = db.Base
engine = create_engine(db.database_url)

class Sedan(Base):
    __tablename__ = 'sedancar'

    id_car = Column(Integer, primary_key=True)
    car_model = Column(String)
    description = Column(String)
    price = Column(Integer)


class Coupe(Base):
    __tablename__ = 'coupecar'

    id_car = Column(Integer, primary_key=True)
    car_model = Column(String)
    description = Column(String)
    price = Column(Integer)


class Suv(Base):
    __tablename__ = 'suvcar'

    id_car = Column(Integer, primary_key=True)
    car_model = Column(String)
    description = Column(String)
    price = Column(Integer)


class Sportcar(Base):
    __tablename__ = 'sportcar'

    id_car = Column(Integer, primary_key=True)
    car_model = Column(String)
    description = Column(String)
    price = Column(Integer)


class Cabrio(Base):
    __tablename__ = 'cabriocar'

    id_car = Column(Integer, primary_key=True)
    car_model = Column(String)
    description = Column(String)
    price = Column(Integer)

class Wagon(Base):
    __tablename__ = 'wagoncar'

    id_car = Column(Integer, primary_key=True)
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



class Sell_customer(Base):
    __tablename__ = 'sell_customers'

    id_customer = Column(Integer, primary_key=True)
    phone = Column(Integer)
    ordered_car = Column(String)
    user_id = Column(Integer, ForeignKey('users.id_user'), nullable=False)
    creating_date = Column(DateTime, default=datetime.datetime.now)

class Rent_customer(Base):
    __tablename__ = 'rent_customers'

    id_customer = Column(Integer, primary_key=True)
    phone = Column(Integer)
    ordered_car = Column(String)
    user_id = Column(Integer, ForeignKey('users.id_user'), nullable=False)
    user = relationship('User', backref=backref('rent_customers', cascade='all,delete'))
    creating_date = Column(DateTime, default=datetime.datetime.now)


Session = sessionmaker(engine)
DBSession = Session()

