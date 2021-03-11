from celery.bin.beat import beat
from tasks import app
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)
app.config_from_object('config')

# @app.on_after_configure.connect
# def setup_periodic_tasks(**kwargs):
#     kwargs['sender'].add_periodic_task(10.0, ping.s(), name='ping every 10')


# @app.task
# def ping():
#     logger.info('ping')


if __name__ == '__main__':
    beat(app=app).run(
        loglevel='INFO'
    )
