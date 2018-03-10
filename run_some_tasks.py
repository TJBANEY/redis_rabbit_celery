from tasks import app
import datetime
from datetime import datetime, timedelta
from celery.utils.log import get_logger
logger = get_logger(__name__)

@app.task
def add(x, y):
    return x + y

# Runs the Celery worker server
# celery -A tasks worker --loglevel=info

# http://docs.celeryproject.org/en/latest/userguide/calling.html#guide-calling

add.delay(5, 6)

@app.task
def error_handler(uuid):
    result = AsyncResult(uuid)
    exc = result.get(propagate=False)
    print('Task {0} raised exception: {1!r}\n{2!r}'.format(
          uuid, exc, result.traceback))


# Adds callback, parent task, ADD, will give its output "9" to its child as a parameter
add.apply_async((3,6), link=add.s(20))

# sets earliest execution time to be in 3 seconds
add.apply_async((2, 2), countdown=3)

# The task is guaranteed to be executed at some time after the specified date and
# time, but not necessarily at that exact time. Possible reasons for broken
# deadlines may include many items waiting in the queue, or heavy network latency.

# While countdown is an integer, eta must be a datetime object
tomorrow = datetime.utcnow() + timedelta(days=1)
add.apply_async((2, 2), eta=tomorrow)

# expiration
add.apply_async((10, 10), expires=60)
add.apply_async((10, 10), kwargs, expires=datetime.now() + timedelta(days=1)

# On Message
# For long-running tasks to send task progress
@app.task(bind=True)
def hello(self, a=3, b=3):
    time.sleep(1)
    self.update_state(state="PROGRESS", meta={'progress': 50})
    time.sleep(1)
    self.update_state(state="PROGRESS", meta={'progress': 90})
    time.sleep(1)
    return 'hello world: %i' % (a+b)

def on_raw_message(body):
    print(body)

r = hello.apply_async()
print(r.get(on_message=on_raw_message, propagate=False))

# Expected Output
# >>> output
# {'task_id': '5660d3a3-92b8-40df-8ccc-33a5d1d680d7',
#  'result': {'progress': 50},
#  'children': [],
#  'status': 'PROGRESS',
#  'traceback': None}
# {'task_id': '5660d3a3-92b8-40df-8ccc-33a5d1d680d7',
#  'result': {'progress': 90},
#  'children': [],
#  'status': 'PROGRESS',
#  'traceback': None}
# {'task_id': '5660d3a3-92b8-40df-8ccc-33a5d1d680d7',
#  'result': 'hello world: 10',
#  'children': [],
#  'status': 'SUCCESS',
#  'traceback': None}
# hello world: 6

# Message Sending Retry

# To disable Retry
add.apply_async((2, 2), retry=False)

# http://docs.celeryproject.org/en/latest/userguide/calling.html#retry-policy

# Handling Exceptions

try:
    add.delay(2, 2)
except add.OperationalError as exc:
    logger.exception('Sending task raised: %r', exc)

# Example setting a custom serializer for a single task invocation
add.apply_async((10, 10), serializer='json')

# Compression  "Celery can compress the messages using either gzip, or bzip2"
# http://docs.celeryproject.org/en/latest/userguide/calling.html#compression

# Connections
# http://docs.celeryproject.org/en/latest/userguide/calling.html#connections

# Routing Options  "Celery can route tasks to different queues."
# http://docs.celeryproject.org/en/latest/userguide/calling.html#routing-options
