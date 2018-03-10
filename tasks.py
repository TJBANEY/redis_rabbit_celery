from celery import Celery

# Arguments = (current module, message broker)
app = Celery('tasks', broker='redis://localhost')

@app.task
def add(x, y):
    return x + y

# Runs the Celery worker server
# celery -A tasks worker --loglevel=info

# Task Cheatsheat

# apply_async(args[, kwargs[, …]])
# >>> Sends a task message.

# delay(*args, **kwargs)
# >>> Shortcut to send a task message, but doesn’t support execution options.

# calling (__call__)
# >>> Applying an object supporting the calling API (e.g., add(2, 2)) means that the 
#     task will not be executed by a worker, but in the current process instead
#     (a message won’t be sent).

# T.delay(arg, kwarg=value)
# Star arguments shortcut to .apply_async. (.delay(*args, **kwargs) calls .apply_async(args, kwargs)).

# T.apply_async((arg,), {'kwarg': value})
# T.apply_async(countdown=10)
# executes in 10 seconds from now.

# T.apply_async(eta=now + timedelta(seconds=10))
# executes in 10 seconds from now, specified using eta

# T.apply_async(countdown=60, expires=120)
# executes in one minute from now, but expires after 2 minutes.

# T.apply_async(expires=now + timedelta(days=2))
# expires in 2 days, set using datetime.
