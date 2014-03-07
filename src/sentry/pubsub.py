import json
import logging
import gevent
import redis

from collections import defaultdict
from gevent.pool import Pool
from fnmatch import fnmatch


class PubSub(object):
    def __init__(self, redis_url, logger=logging.getLogger('sentry.pubsub')):
        self.logger = logger

        self._redis_url = redis_url
        self._gpool = Pool()
        self._callbacks = defaultdict(set)
        self._redis = self.get_connection()
        self._pubsub = self._redis.pubsub()
        self._spawn(self._redis_listen)

    def get_connection(self):
        return redis.from_url(self._redis_url)

    def publish(self, channel, data):
        self._spawn(self._publish_msg, channel, data)
        gevent.sleep(0)

    def subscribe(self, channel, callback):
        self._callbacks[channel].add(callback)
        self.logger.info(
            'Channel {%s} has %d subscriber(s)', channel,
            len(self._callbacks[channel]))
        gevent.sleep(0)

    def unsubscribe(self, channel, callback):
        try:
            self._callbacks[channel].remove(callback)
        except KeyError:
            return

        self.logger.info(
            'Channel {%s} has %d subscriber(s)',
            channel, len(self._callbacks[channel]))
        gevent.sleep(0)

    def _spawn(self, *args, **kwargs):
        return self._gpool.spawn(*args, **kwargs).link_exception(self._log_error)

    def _log_error(self, greenlet):
        self.logger.error(unicode(greenlet.exception))

    def _publish_msg(self, channel, data):
        self._redis.publish(channel, json.dumps(data))

    def _process_msg(self, msg):
        if msg.get('type') in ('psubscribe', 'psubscribe'):
            return

        channel = msg['channel']
        data = json.loads(msg['data'])
        # XXX(dcramer): this code can be run concurrently so its important
        # to note that callbacks can change size/contents during iteration
        for pattern, callbacks in self._callbacks.items():
            if not fnmatch(channel, pattern):
                continue
            # because callbacks is shared, we copy the set into a new list
            # to ensure it doesnt change during iteration
            for cb in list(callbacks):
                self._spawn(cb, data)
            gevent.sleep(0)

    def _redis_listen(self):
        self._pubsub.psubscribe('*')
        for msg in self._pubsub.listen():
            try:
                self._spawn(self._process_msg, msg)
            except Exception as exc:
                self.logger.warn(
                    'Could not process message: %s', exc, exc_info=True)
            gevent.sleep(0)
