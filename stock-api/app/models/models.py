from app.extensions import db
from sqlalchemy import Enum


class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    base_ticket = db.Column(db.String)
    tickets = db.relationship('Ticket', backref='stock', lazy=True)


    def __init__(self, name : str, base_ticket: str):
        self.name = name
        self.base_ticket = base_ticket

    def __repr__(self):
        return f"<Stock {self.name}>"

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticket = db.Column(db.String, nullable=False)
    market = db.Column(Enum("frac", "normal", name="market_type", create_type=True), nullable=False)
    stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'),
                          nullable=False)
    def __init__(self, ticket : str, stock_id: int, market: str):
        self.ticket = ticket
        self.stock_id = stock_id
        self.market = market

    def __repr__(self):
        return f"<Ticket {self.ticket}>"
    
    @classmethod
    def find_by_ticket(cls, session, ticket):
      return session.query(cls).filter_by(ticket=ticket).one()
    
    @classmethod
    def find_by_id(cls, session, id):
      return session.query(cls).filter_by(id=id).one()

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type_of = db.Column(Enum("buy", "sell", name="transaction_type", create_type=True)) 
    quantity = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime)
    value = db.Column(db.Float, nullable=False)
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'),
                          nullable=False)

    def __init__(self, type_of: str, quantity: int, date: str, value: float, ticket_id : int):
        self.type_of = type_of
        self.quantity = quantity
        self.date = date
        self.value = value
        self.ticket_id = ticket_id

    def __repr__(self):
        return f"<Transaction {self.ticket_id}>"