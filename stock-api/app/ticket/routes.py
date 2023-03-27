from app.ticket import bp
from app.extensions import db
from app.models.models import Stock, Ticket
from flask import request

@bp.route('/', methods=['GET'])
def list_tickets():
    tickets = db.session.query(Ticket, Stock).join(Ticket, Ticket.stock_id == Stock.id).all()
    response = [
      {
          'ticket': ticket.ticket,
          'id': ticket.id,
          'name': stock.name
      } 
      for ticket, stock in tickets
    ]
    return {"count": len(response), "items": response}

@bp.route('/', methods=['POST'])
def ticket_list():
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
        return {"message": f"ticket {new_ticket.ticket} has been created successfully."}
    else:
        return {"error": "The request payload is not in JSON format"}