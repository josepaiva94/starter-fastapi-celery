import sys
from time import sleep
import ffmpeg

from celery import current_task

from .celery_app import celery_app


@celery_app.task(acks_late=True)
def test_celery(word: str) -> str:
    for i in range(1, 11):
        sleep(1)
        current_task.update_state(state='PROGRESS',
                                  meta={'process_percent': i*10})
    generate_thumbnail('/app/in.mp4', 'out.jpg', 0.1, 120)
    return f"test task return {word}"


def generate_thumbnail(in_filename, out_filename, time, width):
    try:
        (
            ffmpeg
            .input(in_filename, ss=time)
            .filter('scale', width, -1)
            .output(out_filename, vframes=1)
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
    except ffmpeg.Error as e:
        print(e.stderr.decode(), file=sys.stderr)
        sys.exit(1)

