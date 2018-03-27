from sentry.utils.runner import configure; configure()

import concurrent.futures

import pprint
import sentry
from sentry.tsdb.redis import RedisTSDB
from sentry.tsdb.dummy import DummyTSDB
from sentry.utils.services import MultipleServiceBackend


def callback(name, args, kwargs, futures):
    results = []
    for future in futures:
        results.append(future.result())
    pprint.pprint([name, args, kwargs, results])


tsdb = MultipleServiceBackend(
    concurrent.futures.ThreadPoolExecutor(),
    [RedisTSDB(), DummyTSDB()],
    set([
        'get_range',
    ]),
    callback,
)
