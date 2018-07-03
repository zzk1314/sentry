from __future__ import absolute_import

import random
import uuid
from collections import defaultdict, deque

from confluent_kafka import Consumer, TopicPartition


class SynchronizedConsumer(object):
    def __init__(self, consumer_configuration, topics, offsets_consumer_configuration, offsets_topics):
        consumer_configuration = self.__validate_consumer_configuration(consumer_configuration)
        offsets_consumer_configuration = self.__validate_offsets_consumer_configuration(offsets_consumer_configuration)

        self.__consumer = Consumer(consumer_configuration)
        self.__consumer.subscribe(topics)

        self.__offsets_consumer = Consumer(offsets_consumer_configuration)
        self.__offsets_consumer.subscribe(offsets_topics)  # TODO: This should warn if things move around

        self.__offsets = {}
        self.__buffers = defaultdict(deque)

    def __validate_consumer_configuration(self, configuration):
        requirements = {
            'enable.auto.offset.store': 'false',
            'enable.partition.eof': 'false',  # this could be handled without too much work
        }

        for key, value in requirements.items():
            assert configuration.setdefault(key, value) == value

        return configuration

    def __validate_offsets_consumer_configuration(self, configuration):
        requirements = {
            'offset.store.method': 'none',
            'enable.auto.offset.store': 'false',
            'enable.partition.eof': 'false',  # this could be handled without too much work
            'default.topic.config': {
                'auto.offset.reset': 'earliest',
            },
        }

        for key, value in requirements.items():
            assert configuration.setdefault(key, value) == value

        assert 'group.id' not in configuration
        configuration['group.id'] = uuid.uuid1.hex()

        return configuration

    def __poll_consumer(self, timeout=None):
        message = self.__consumer.poll(timeout)
        if message is None:
            return

        if message.error() is not None:
            raise Exception(message.error())

        self.__buffers[(message.topic(), message.partition())].append(message)

        if not self.__offsets((message.topic(), message.partition())) > message.offset():
            self.__consumer.pause([
                TopicPartition(message.topic(), message.partition(), message.offset()),
            ])

    def __decode_offsets_message(self, message):
        raise NotImplementedError

    def __poll_offsets_consumer(self, timeout=None):
        message = self.__offsets_consumer.poll(timeout)
        if message is None:
            return

        if message.error() is not None:
            raise Exception(message.error())

        # TODO: Check the group and topic against the configuration.
        group, topic, partition, offset = self.__decode_offsets_message(message)

        self.__offsets[(topic, partition)] = offset

    def __get_message(self):
        buffers = sorted(self.__buffers.items(), key=lambda b: random.random())
        for (topic, partition), buffer in buffers:
            if not buffer:
                continue

            message = buffer[0]
            if not self.__offsets[(message.topic(), message.partition())] > message.offset():
                continue

            assert buffer.popleft() is message

            if not buffer:
                self.__consumer.resume([
                    TopicPartition(message.topic(), message.partition(), message.offset()),
                ])

            # TODO: Update the internal position marker for this partition for later commit.

            return message

    def poll(self, timeout=None):
        # TODO: These poll methods need to execute concurrently.
        self.__poll_offsets_consumer(timeout)
        self.__poll_consumer(timeout)
        return self.__get_message()

    def commit(self):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError
