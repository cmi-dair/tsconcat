import datetime
import time
from contextlib import contextmanager


@contextmanager
def timeprint(title: str):
    print(f'Start: {title}')
    start = time.perf_counter()
    yield
    duration = time.perf_counter() - start
    print(f'Done: {title} - {datetime.timedelta(seconds=duration)}')
