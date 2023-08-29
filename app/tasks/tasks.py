from celery import Celery

from celery_dijkstra import calculate_path

app = Celery('tasks', backend='redis://localhost:6379/0', broker='amqp://rabbitmq:rabbitmq@localhost//')


@app.task
def add(table_id):
    return calculate_path(table_id)
