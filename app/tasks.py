from celery import Celery
#
from celery_dijkstra import calculate_path
#
app = Celery('tasks', backend='redis://localhost:6379/0', broker='amqp://rabbitmq:rabbitmq@localhost//')


def sum2(x,y):
    return x+y

@app.task
def add(table_id,point_start,point_finish):
    return calculate_path(table_id,point_start,point_finish)
