#!/bin/bash
set -ex

if [ ! -f /.bootstrapped-lib ]; then
    pip install -vvv -e .[dev,tests]
    yarn install
    touch /.bootstrapped-lib
    make develop
    echo "SUCCESS: Libraries and dependencies installed!"
fi

if [ ! -f /.bootstrapped-sentry ]; then
    sentry upgrade --noinput
    # sentry createuser --email=root@localhost --password=admin --superuser --no-input
    echo "User created

    login: root@localhost
    password: admin


    "
    touch /.bootstrapped-sentry
    echo "SUCCESS: Sentry development environment set up" # && exit 0
fi

exec "$@"
