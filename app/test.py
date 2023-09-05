from app.tasks import add
import uuid


def generate_id():
    return uuid.uuid4()

table_id = generate_id()

add.delay(table_id)