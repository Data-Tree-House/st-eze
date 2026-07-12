import time

from celery import Celery

from constants import c

app = Celery(
    "worker",
    broker=f"amqp://{c.rabbitmq_default_user}:{c.rabbitmq_default_pass}@{c.rmq_host}:{c.rmq_port}//",
    backend="db+sqlite:///results.db",
)


# https://docs.celeryq.dev/en/stable/userguide/configuration.html#configuration
app.conf.update(
    # Only fetch one message at a time... don't buffer ahead
    worker_prefetch_multiplier=1,
    #  Only one task can run concurrently per worker process
    worker_concurrency=1,
    # Acknowledge the task AFTER it's done, not when it's received
    task_acks_late=True,
    # If the worker crashes mid-task, requeue it
    task_reject_on_worker_lost=True,
)


@app.task
def add(x, y):
    return x + y


@app.task
def refresh_task():
    time.sleep(10)
    return 10
