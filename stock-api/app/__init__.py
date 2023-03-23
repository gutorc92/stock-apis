import os
from flask import Flask
import pika
import json
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate
from flask_cors import CORS
from app.extensions import db

# create the extension

# @app.route('/tickets', methods=['GET'])
# def list_tickets():
#     tickets = db.session.query(Ticket, Stock).join(Ticket, Ticket.stock_id == Stock.id).all()
#     print(tickets)
#     response = [
#       {
#           'ticket': ticket.ticket,
#           'id': ticket.id,
#           'name': stock.name
#       } 
#       for ticket, stock in tickets
#     ]
#     return {"count": len(response), "items": response}

# @app.route('/stock/<id>/ticket', methods=['GET', 'POST'])
# def ticket_list(id):
#     if request.method == 'POST':
#         if request.is_json:
#             data = request.get_json()
#             market = 'normal'
#             if data['ticket'][-1] == 'F':
#                 market = 'frac'
#             new_ticket = Ticket(
#                 ticket=data['ticket'],
#                 stock_id=data['stock_id'],
#                 market=market
#               )
#             db.session.add(new_ticket)
#             db.session.commit()
#             return {"message": f"car {new_ticket.ticket} has been created successfully."}
#         else:
#             return {"error": "The request payload is not in JSON format"}

#     elif request.method == 'GET':
#         tickets = Ticket.query.filter_by(stock_id = id).all()
#         response = [
#           {
#             'ticket': ticket.ticket,
#             'id': ticket.id
#           } 
#           for ticket in tickets]
#         return {"count": len(response), "tickets": response}
    
# @app.route('/transaction/ticket/<id>/purchase', methods=['GET', 'POST'])
# def purchase(id):
#     if request.method == 'POST':
#         if request.is_json:
#             data = request.get_json()
#             new_transcation = Transaction(
#                 type_of='buy', 
#                 quantity=data['quantity'], 
#                 date=datetime.strptime(data['date'], '%d/%m/%Y'), 
#                 value=data['value'], 
#                 ticket_id=data['ticket_id']
#               )
#             db.session.add(new_transcation)
#             db.session.commit()
#             ticket = Ticket.find_by_id(db.session, data['ticket_id'])
#             connection = pika.BlockingConnection(pika.ConnectionParameters(
#                 'localhost',
#                 '5672',
#                 '/',
#                 pika.PlainCredentials('user', '123456')
#               )
#             )
#             channel = connection.channel()
#             channel.queue_declare(queue='log-messages', durable=True)
#             channel.basic_publish(
#                       exchange='',
#                       routing_key='log-messages',
#                       body=json.dumps({
#                         'ticket_id': ticket.id,
#                         'ticket': ticket.ticket,
#                         'date': data['date']
#                       })
#             )
#             connection.close()
#             return {"message": f"car {new_transcation.ticket_id} has been created successfully."}
#         else:
#             return {"error": "The request payload is not in JSON format"}

#     elif request.method == 'GET':
#         transcations = Transaction.query.filter_by(ticket_id = id).all()
#         response = [
#           {
#             'ticket_id': transcation.ticket_id,
#             'id': transcation.id
#           } 
#           for transcation in transcations]
#         return {"count": len(response), "items": response}

# @app.route("/")
# def index():
#     secret_key = app.config.get("SECRET_KEY")
#     return f"The configured secret key is {secret_key}."

def create_app(config_class=Config):
  # create the app
  app = Flask(__name__)
  CORS(app)
  env_config = os.getenv("APP_SETTINGS", "config.DevelopmentConfig")
  app.config.from_object(env_config)

  db.init_app(app)
  migrate = Migrate(app, db)
  from app.stock import bp as stock_bp
  from app.main import bp as main_bp
  main_bp.register_blueprint(stock_bp)
  app.register_blueprint(main_bp, url_prefix='/api')

  @app.route('/test/')
  def test_page():
      return '<h1>Testing the Flask Application Factory Pattern</h1>'
  return app