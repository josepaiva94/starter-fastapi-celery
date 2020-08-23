import logging

from fastapi import FastAPI, BackgroundTasks

from worker.celery_app import celery_app


log = logging.getLogger(__name__)

app = FastAPI()


def celery_on_message(body):
    log.warning(body)


def background_on_message(task):
    log.warning(task.get(on_message=celery_on_message, propagate=False))


@app.get('/{word}')
async def root(word: str, background_task: BackgroundTasks):
    task_name = 'app.worker.celery_worker.test_celery'

    task = celery_app.send_task(task_name, args=[word])
    background_task.add_task(background_on_message, task)
    print(task)

    return {'message': 'Word received'}
