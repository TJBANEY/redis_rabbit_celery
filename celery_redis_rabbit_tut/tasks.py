from celery import Celery

# Arguments = (current module, message broker)
app = Celery('tasks', broker='redis://localhost')
