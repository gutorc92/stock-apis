import os
import pika
import json
from datetime import datetime
from flask import request
from app import app, db
basedir = os.path.abspath(os.path.dirname(__file__))
from models.models import Stock, Ticket, Transaction

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


@app.route('/tickets', methods=['GET'])
def list_tickets():
    tickets = db.session.query(Ticket, Stock).join(Ticket, Ticket.stock_id == Stock.id).all()
    print(tickets)
    response = [
      {
          'ticket': ticket.ticket,
          'id': ticket.id,
          'name': stock.name
      } 
      for ticket, stock in tickets
    ]
    return {"count": len(response), "items": response}

@app.route('/stock/<id>/ticket', methods=['GET', 'POST'])
def ticket_list(id):
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            market = 'normal'
            if data['ticket'][-1] == 'F':
                market = 'frac'
            new_ticket = Ticket(
                ticket=data['ticket'],
                stock_id=data['stock_id'],
                market=market
              )
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
    
@app.route('/transaction/ticket/<id>/purchase', methods=['GET', 'POST'])
def purchase(id):
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_transcation = Transaction(
                type_of='buy', 
                quantity=data['quantity'], 
                date=datetime.strptime(data['date'], '%d/%m/%Y'), 
                value=data['value'], 
                ticket_id=data['ticket_id']
              )
            db.session.add(new_transcation)
            db.session.commit()
            ticket = Ticket.find_by_id(db.session, data['ticket_id'])
            connection = pika.BlockingConnection(pika.ConnectionParameters(
                'localhost',
                '5672',
                '/',
                pika.PlainCredentials('user', '123456')
              )
            )
            channel = connection.channel()
            channel.queue_declare(queue='log-messages', durable=True)
            channel.basic_publish(
                      exchange='',
                      routing_key='log-messages',
                      body=json.dumps({
                        'ticket_id': ticket.id,
                        'ticket': ticket.ticket,
                        'date': data['date']
                      })
            )
            connection.close()
            return {"message": f"car {new_transcation.ticket_id} has been created successfully."}
        else:
            return {"error": "The request payload is not in JSON format"}

    elif request.method == 'GET':
        transcations = Transaction.query.filter_by(ticket_id = id).all()
        response = [
          {
            'ticket_id': transcation.ticket_id,
            'id': transcation.id
          } 
          for transcation in transcations]
        return {"count": len(response), "items": response}

@app.route("/")
def index():
    secret_key = app.config.get("SECRET_KEY")
    return f"The configured secret key is {secret_key}."

if __name__ == '__main__':
    app.run()