from celery.bin.worker import worker
from tasks import app

app.config_from_object('config')

if __name__ == '__main__':
    worker(app=app).run(
        queues='default,test',
        loglevel='INFO'
    )
