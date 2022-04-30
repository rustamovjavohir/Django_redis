import time

from celery import Celery
from celery import shared_task
from celery.schedules import crontab
from django.conf import settings

app = Celery('Django_redis',
             broker=settings.CELERY_BROKER_URL,
             backend=settings.CELERY_RESULT_BACKEND,
             # backend='redis://localhost:6379/0',
             )


@app.task(name='add', track_started=True)
def add(x, y):
    print('Ishladiiii')
    return x + y


@shared_task(name='multiple_two', ignore_result=True)
def multiple_two(x):
    print('multiple')
    return 2 * x


@shared_task(bind=True)
def test_func(self):
    time.sleep(5)
    # print('time sleap')
    # for i in range(10):
    #     time.sleep(1)
    #     print(i)
    return 'Done'


@shared_task
def this_is_my_first_project():
    print("This_is_my_first_project 2")


@app.task
def my_task():
    return "periodic tasks is works"


@app.task
def my_task_as(d, e):
    c = d + e
    return c


@app.task(bind=True, default_retry_delay=5 * 60)
def my_task_retry(self, x, y):
    try:
        return x + y
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)


@shared_task()
def my_sh_task(msg):
    return msg + "!!!"


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(10.0, my_sh_task.s('hello'), name='add every 10')

    # # Calls test('world') every 30 seconds
    # sender.add_periodic_task(30.0, test.s('world'), expires=10)
    #
    # # Executes every Monday morning at 7:30 a.m.
    # sender.add_periodic_task(
    #     crontab(hour=7, minute=30, day_of_week=1),
    #     test.s('Happy Mondays!'),
    # )


app.conf.beat_schedule = {
    'add-every-15-seconds': {
        'task': 'test_celery.tasks.my_sh_task',
        'schedule': 15,
        'args': ('Hello',),
    },
}

app.conf.beat_schedule = {
    'my_task-every-20-seconds': {
        'task': 'test_celery.tasks.my_task',
        'schedule': 20,
        'args': [10, 5],
    },
}

app.conf.beat_schedule = {
    'multiple_two-every-20-seconds': {
        'task': 'test_celery.tasks.multiple_two',
        'schedule': crontab(minute='*/1'),
        'args': (10,),
    },
}
