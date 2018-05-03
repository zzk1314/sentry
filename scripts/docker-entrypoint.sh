#!/bin/bash
set -ex

if [ ! -f /.bootstrapped ]; then
    SENTRY_LIGHT_BUILD=1 pip install -vvv -e .[dev,tests]
    yarn install
    touch /.bootstrapped
    echo "bootstrapped!"
fi

if [ ! -f /.bootstrapped-sentry ]; then

    sentry upgrade --noinput
    sentry createuser --email=root@localhost --password=admin --superuser --no-input
    echo "sentry success"
    touch /.bootstrapped-sentry
    echo "done" # && exit 0
fi

exec "$@"
