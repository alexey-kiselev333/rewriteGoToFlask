import time

from amqp import channel
from kombu import Connection, Exchange, Queue, Producer, Consumer
import settings as s

rabbit_url = s.RABBIT_URL

conn = Connection('amqp://rabbitmq:rabbitmq@localhost:5672//')

channel = conn.channel()

exchange = Exchange('PathQuery', type='direct')
queue = Queue('PathQuery', exchange=exchange, routing_key='PathQuery')

def callback(body, message):
    print(body)
    producer = Producer(exchange=exchange, channel=channel, routing_key=s.routing_key)
    queueResp = Queue(name=s.Q_NAME, exchange=exchange, routing_key=s.routing_key)
    queueResp.maybe_bind(conn)
    queueResp.declare()

    producer.publish("===>>> " + body)
    message.ack()

with Connection('amqp://rabbitmq:rabbitmq@localhost:5672//') as c:
    while True:
        with Consumer(c.default_channel, queues=[queue], callbacks=[callback]):
            c.drain_events()
