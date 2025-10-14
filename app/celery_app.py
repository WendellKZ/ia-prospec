from celery import Celery
from kombu import Queue
from config import Config

def make_celery(app, eager: bool=False):
    celery = Celery(app.import_name, broker=Config.CELERY_BROKER_URL, backend=Config.CELERY_RESULT_BACKEND)
    celery.conf.update(
        task_queues=(Queue('prospecting'), Queue('enrichment'), Queue('seasonality')),
        task_default_queue='prospecting',
        task_track_started=True,
        worker_max_tasks_per_child=100,
    )
    celery.conf.task_always_eager = bool(eager)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    celery.Task = ContextTask
    return celery
