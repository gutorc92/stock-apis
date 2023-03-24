from app.ticket import bp
from app.extensions import db
from app.models.models import Stock, Ticket

@bp.route('/', methods=['GET'])
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