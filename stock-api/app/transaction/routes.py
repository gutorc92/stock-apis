from app.transaction import bp
from app.extensions import db
from app.models.models import Stock, Ticket, Transaction
from flask import request
import pika
import json
from datetime import datetime

@bp.route('/ticket/<id>', methods=['GET'])
def list(id):
    transcations = Transaction.query.filter_by(ticket_id = id).all()
    response = [
      {
        'ticket_id': transcation.ticket_id,
        'id': transcation.id
      } 
      for transcation in transcations]
    return {"count": len(response), "items": response}

@bp.route('/ticket/<id>/purchase', methods=['POST'])
def purchase(id):
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