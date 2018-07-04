from __future__ import absolute_import

from confluent_kafka import Producer, Consumer
import subprocess


def run_kafka_topic_command(args):
    subprocess.check_call(['docker', 'exec', 'kafka', 'kafka-topics', '--zookeeper', 'zookeeper:2181'] + list(args))


def test_kafka():
    run_kafka_topic_command(['--create', '--topic', 'events', '--replication-factor', '1', '--partitions', '3'])

    try:
        expected = set()
        producer = Producer({'bootstrap.servers': 'localhost:9092'})
        for i in xrange(10):
            value = b'{}'.format(i)
            producer.produce('events', value, key=b'{}'.format(i))
            expected.add(value)
            producer.poll(1)
        producer.flush()

        consumer = Consumer({
            'bootstrap.servers': 'localhost:9092',
            'group.id': 'ephemeral',
            'offset.store.method': 'none',
            'enable.auto.offset.store': 'false',
            'enable.partition.eof': 'false',
            'default.topic.config': {
                'auto.offset.reset': 'earliest',
            },
        })
        consumer.subscribe(['events'])

        actual = set()
        while expected - actual:
            message = consumer.poll(1)
            if message is None:
                continue

            if message.error():
                raise Exception(message.error())

            assert message.value() in expected
            actual.add(message.value())
    finally:
        run_kafka_topic_command(['--delete', '--topic', 'events'])
