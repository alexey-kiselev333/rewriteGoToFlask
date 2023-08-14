import time

from amqp import channel
from kombu import Connection, Exchange, Queue, Producer, Consumer
import settings as s

rabbit_url = s.RABBIT_URL

conn = Connection('amqp://rabbitmq:rabbitmq@localhost:5672//')

channel = conn.channel()

exchange = Exchange('DijkstraPathQuery', type='direct')
queue = Queue('DijkstraPathQuery', exchange=exchange, routing_key='DijkstraPathQuery')

def callback(body, message):
    print(body)
    producer = Producer(exchange=exchange, channel=channel, routing_key=s.routing_key)
    queue = Queue(name=s.Q_NAME, exchange=exchange, routing_key=s.routing_key)
    queue.maybe_bind(conn)
    queue.declare()

    producer.publish("===>>> " + time.strftime("%Y-%m-%d %H:%M:%S"))
    message.ack()

with Connection('amqp://rabbitmq:rabbitmq@localhost:5672//') as c:
    while True:
        with Consumer(c.default_channel, queues=[queue], callbacks=[callback]):
            c.drain_events()
