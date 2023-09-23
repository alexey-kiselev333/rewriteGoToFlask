import threading
import uuid

from amqp import channel
from kombu import Connection, Exchange, Queue, Producer, Consumer
from tasks import sum2
from tasks import add
from ast import literal_eval
from celery_dijkstra import dist
import json

print('dsfsfs', sum2(2, 1))
import rethinkdb as r

import settings as s

rabbit_url = s.RABBIT_URL
from pathlib import Path

conn = Connection('amqp://rabbitmq:rabbitmq@localhost:5672//')

channel = conn.channel()
rdb = r.RethinkDB()
connReth = rdb.connect(host='localhost', port=28015)
exchange = Exchange('PathQuery', type='direct')
queue = Queue('PathQuery', exchange=exchange, routing_key='PathQuery')


def callback(body, message):
    producer = Producer(exchange=exchange, channel=channel, routing_key=s.routing_key)
    queueResp = Queue(name=s.Q_NAME, exchange=exchange, routing_key=s.routing_key)
    queueResp.maybe_bind(conn)
    queueResp.declare()
    # print(body)
    body = json.loads(body)
    point_start = body["point_start"]
    print(point_start)

    point_finish = body["point_finish"]

    print(point_finish)
    table_id = uuid.uuid4()

    if not rdb.db('whoosh').table_list().contains(str(table_id)).run(connReth):
        rdb.db('whoosh').table_create(str(table_id)).run(connReth)
    thread = threading.Thread(target=add.delay, args=(table_id, point_start, point_finish))

    thread.start()


    feed = rdb.db('whoosh').table(str(table_id)).changes().run(connReth)
    flag = False
    for change in feed:
        last_vertex = literal_eval(change["new_val"]["result"])[-1]

        last_vertex_info = rdb.db('whoosh').table('graph').filter({'index': int(last_vertex)}).run(connReth)

        for element in last_vertex_info:
            if dist(point_finish, element) < 0.0001:
                flag = True
        if flag:
            print(change["new_val"]["result"])
            producer.publish(change["new_val"]["result"])
            break

    thread.join()


    message.ack()


with Connection('amqp://rabbitmq:rabbitmq@localhost:5672//') as c:
    while True:
        with Consumer(c.default_channel, queues=[queue], callbacks=[callback]):
            c.drain_events()
