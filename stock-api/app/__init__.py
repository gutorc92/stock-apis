import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate
from flask_cors import CORS
from app.extensions import db
from app.stock import bp as stock_bp
from app.main import bp as main_bp
from app.ticket import bp as ticket_bp
from app.transaction import bp as transaction_bp

main_bp.register_blueprint(stock_bp)
main_bp.register_blueprint(ticket_bp, url_prefix='/ticket')
main_bp.register_blueprint(transaction_bp, url_prefix='/transaction')

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

def create_app(config_class=Config):
  # create the app
  app = Flask(__name__)
  CORS(app)
  env_config = os.getenv("APP_SETTINGS", "config.DevelopmentConfig")
  app.config.from_object(env_config)

  db.init_app(app)
  migrate = Migrate(app, db)
    
  app.register_blueprint(main_bp, url_prefix='/api')

  @app.route('/test/')
  def test_page():
      return '<h1>Testing the Flask Application Factory Pattern</h1>'
  return app