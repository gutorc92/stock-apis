from sqlalchemy import Column, Integer, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Price(Base):
    __tablename__ = 'price'

    id = Column(Integer, primary_key=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    adj_close = Column(Float)
    volume =  Column(Integer)
    date = Column(DateTime)
    ticket_id = Column(Integer)

    def __init__(self, ticket_id: int, date: datetime, **kwargs) -> None:
        self.ticket_id = ticket_id
        print('kwargs', kwargs)
        self.open = kwargs.get('Open', 0.0)
        self.high = kwargs.get('High', 0.0)
        self.low = kwargs.get('Low', 0.0)
        self.close = kwargs.get('Close', 0.0)
        self.adj_close = kwargs.get('Adj Close', 0.0)
        self.volume = kwargs.get('Volume', 0)
        self.date = date

    def __repr__(self):
        return f'Ticket {self.ticket_id}'