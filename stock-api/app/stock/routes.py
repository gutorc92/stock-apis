from app.stock import bp
# from flask import Blueprint
from flask import request
# from app import db
from app.extensions import db
from app.models.models import Stock, Ticket

@bp.route("/stock", methods=['POST', 'GET'])
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

@bp.route('/stock/<id>', methods=['GET', 'PATCH'])
def stock(id):
    if request.method == 'GET':
      stock = Stock.query.filter_by(Stock.id == id)
      response = {
        'name': stock.name,
        'ticket': stock.base_ticket,
        'id': stock.id
      }
      return {"item": response}
    elif request.method == 'PATCH':
      if request.is_json:
        data = request.get_json()
        stmt = Stock.query.filter_by(Stock.id == id)
        stock = db.session.scalars(stmt).one()
        stock.name = data['name']
        stock.base_ticket = data['base_ticket']
        db.session.commit()
        return {'result': True}