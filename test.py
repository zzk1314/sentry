from sentry.utils.runner import configure; configure()

import pprint
import sentry
from sentry.tsdb.redis import RedisTSDB
from sentry.tsdb.dummy import DummyTSDB
from sentry.utils.services import MultipleServiceBackend


def callback(request, responses, *a, **k):
    results = []
    for backend, response in responses.items():
        results.append((backend, response.result()))
    pprint.pprint((request, results))


tsdb = MultipleServiceBackend(
    [RedisTSDB(), DummyTSDB()],
    set([
        'get_range',
    ]),
    callback,
)
