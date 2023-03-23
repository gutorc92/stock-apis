import pika, sys, os, json
import yfinance as yf
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import Base, Price

def main():
    engine = create_engine('postgresql://postgres:Postgres2022!@localhost:5432/stock', echo=True)
    conn = engine.connect()
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        'localhost',
        '5672',
        '/',
        pika.PlainCredentials('user', '123456')
    ))
    channel = connection.channel()

    channel.queue_declare(queue='log-messages', durable=True)

    def callback(ch, method, properties, body):
        data = json.loads(body)
        start = datetime.strptime(data['date'], '%d/%m/%Y')
        print("start: ", start.strftime('%Y-%m-%d'), "end", datetime.now().strftime('%Y-%m-%d'))
        pd = yf.download(tickers = f"{data['ticket']}.SA",  # list of tickers
                    start = start.strftime('%Y-%m-%d'),         # time period
                    end = datetime.now().strftime('%Y-%m-%d'),
                    interval = "1d",       # trading interval
                    ignore_tz = True,      # ignore timezone when aligning data from different exchanges?
                    prepost = False)
        for index, row in pd.iterrows():
          line = row.to_dict()
          price = Price(data['ticket_id'], index.to_pydatetime(), **line)
          session.add(price)
        session.commit()

    channel.basic_consume(queue='log-messages', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)