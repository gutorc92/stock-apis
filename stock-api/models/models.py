from app import db
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
    stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'),
                          nullable=False)
    def __init__(self, ticket : str, stock_id: int):
        self.ticket = ticket
        self.stock_id = stock_id

    def __repr__(self):
        return f"<Ticket {self.ticket}>"

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    market = db.Column(Enum("frac", "normal", name="market_type", create_type=True), nullable=False)
    type_of = db.Column(Enum("buy", "sell", name="transaction_type", create_type=True)) 
    quantity = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime)
    value = db.Column(db.Float, nullable=False)
    tick_id = db.Column(db.Integer, db.ForeignKey('ticket.id'),
                          nullable=False)

    def __init__(self, ticket : str, base_ticket: str):
        self.ticket = ticket
        self.base_ticket = base_ticket

    def __repr__(self):
        return f"<Transaction {self.name}>"