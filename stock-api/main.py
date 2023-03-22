import os
from flask import request
from app import app, db
basedir = os.path.abspath(os.path.dirname(__file__))
from models.models import Stock, Ticket

from sqlalchemy import select, update

@app.route("/stock", methods=['POST', 'GET'])
def stock_list():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_stock = Stock(name=data['name'], base_ticket=data['base_ticket'])
            db.session.add(new_stock)
            db.session.commit()
            return {"message": f"car {new_stock.name} has been created successfully."}
        else:
            return {"error": "The request payload is not in JSON format"}

    elif request.method == 'GET':
        stocks = Stock.query.all()
        response = [
          {
            'name': stock.name,
            'ticket': stock.base_ticket,
            'id': stock.id,
            'tickets': [ticket.ticket for ticket in Ticket.query.filter_by(stock_id = stock.id)]
          } 
          for stock in stocks]
        return {"count": len(response), "stocks": response}

@app.route('/stock/<id>', methods=['GET', 'PATCH'])
def stock(id):
    if request.method == 'GET':
      stmt = select(Stock).where(Stock.id == id)
      stock = db.session.scalars(stmt).one()
      response = {
        'name': stock.name,
        'ticket': stock.base_ticket,
        'id': stock.id
      }
      return {"item": response}
    elif request.method == 'PATCH':
      if request.is_json:
        data = request.get_json()
        stmt = select(Stock).where(Stock.id == id)
        stock = db.session.scalars(stmt).one()
        stock.name = data['name']
        stock.base_ticket = data['base_ticket']
        db.session.commit()
        return {'result': True}

@app.route('/stock/<id>/ticket', methods=['GET', 'POST'])
def ticket_list(id):
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_ticket = Ticket(ticket=data['ticket'], stock_id=data['stock_id'])
            db.session.add(new_ticket)
            db.session.commit()
            return {"message": f"car {new_ticket.ticket} has been created successfully."}
        else:
            return {"error": "The request payload is not in JSON format"}

    elif request.method == 'GET':
        tickets = Ticket.query.filter_by(stock_id = id).all()
        response = [
          {
            'ticket': ticket.ticket,
            'id': ticket.id
          } 
          for ticket in tickets]
        return {"count": len(response), "tickets": response}

@app.route("/")
def index():
    secret_key = app.config.get("SECRET_KEY")
    return f"The configured secret key is {secret_key}."

if __name__ == '__main__':
    app.run()