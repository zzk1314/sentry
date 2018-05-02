#!/bin/bash
set -ex

if [ ! -f /.bootstrapped ]; then
    SENTRY_LIGHT_BUILD=1 pip install -vvv -e .[dev,tests]
    yarn install
    touch /.bootstrapped
    echo "bootstrapped!"
fi
if [ ! -f /.bootstrapped-sentry ]; then
    sentry init $"SENTRY_CONF"
    # copy over init files with docker-specific setup
    cp sentry-docker/dev/docker-sentry.conf.py $"SENTRY_CONF"/sentry.conf.py
    cp sentry-docker/dev/docker-config.yml $"SENTRY_CONF"/config.yml
    sentry upgrade --noinput
    sentry createuser --email=root@localhost --password=admin --superuser --no-input
    echo "sentry success"
    echo "done" # && exit 0
fi

exec "$@"
