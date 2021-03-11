from celery.app.task import Task
from app import app
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


class TaskBase(Task):
    def run(self, *args, **kwargs):
        logger.info('task base')

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.error(exc)

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        logger.error(exc)

    def on_success(self, retval, task_id, args, kwargs):
        logger.info('task success')

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        logger.info('task done')


@app.task(bind=True, base=TaskBase, queue='test')
def add(self, x, y):
    try:
        logger.info(f'{x}:{y}')
        return x + y
    except Exception as ge:
        logger.info(ge)
        self.retry()


@app.task(queue='default')
def mul(x, y):
    return x * y


@app.task(queue='default')
def xsum(numbers):
    return sum(numbers)


@app.task
def exec_periodic_task():
    """
    调度定时任务
    Args:

    Returns:

    """

    pass


def test_chain():
    chain = add.s(1, 2) | mul.s(2)
    chain.apply_async(queue='default')


def test_link():
    add.apply_async([1, 2], link=mul.s(3))
