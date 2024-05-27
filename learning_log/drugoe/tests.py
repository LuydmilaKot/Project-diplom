from celery import Celery

# from time import sleep

app = Celery(
    "tasks", broker="redis://127.0.0.1:6379/0", backend="db+sqlite:///db.sqlite3"
)


@app.task
def reverse(text):
    # sleep(5)
    return text[::-1]


# celery -A tasks worker --loglevel=info

# reverse.delay("test")

# проверка подключения редиса
#redis cli
#PING - PONG