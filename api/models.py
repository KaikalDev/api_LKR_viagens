from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from dataBase import Base

class User(Base):
    __tablename__ = 'users'
    
    userId = Column(Integer, primary_key=True, index=True)
    user = Column(String)
    password = Column(String)

    trips = relationship("Trip", back_populates="user")

class Trip(Base):
    __tablename__ = 'trips'

    id = Column(Integer, primary_key=True, index=True)
    departureDate = Column(String)
    returnDate = Column(String)
    destiny = Column(String)
    typeDestiny = Column(String)
    typeTrip = Column(String)
    description = Column(String)
    userId = Column(Integer, ForeignKey('users.userId'))

    user = relationship("User", back_populates="trips")
