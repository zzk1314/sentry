#!/bin/bash
set -ex

if [ ! -f /.bootstrapped ]; then
  SENTRY_LIGHT_BUILD=1 pip install -vvv -e .[dev,tests]
  npm install
  sentry init $SENTRY_CONF
  sentry upgrade --noinput
  sentry createuser --email=root@localhost --password=admin --superuser --no-input
  touch /.bootstrapped

  echo "done" && exit 0
fi

exec "$@"
