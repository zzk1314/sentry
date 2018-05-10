FROM python:2.7.14-slim

RUN groupadd -r redis --gid=998 && useradd -r -g redis --uid=998 redis \
    && groupadd -r postgres --gid=999 && useradd -r -g postgres --uid=999 postgres

RUN apt-get update -q=2 \
    && apt-get install -y --no-install-recommends -q=2 \
        clang \
        curl \
        g++ \
        gcc \
        git \
        libffi-dev \
        libjpeg-dev \
        libpq-dev \
        libxml2-dev \
        libxslt-dev \
        libyaml-dev \
        llvm-3.5 \
        bzip2 \
        apt-transport-https \
        # Extra dev tooling
        make \
        vim-nox \
        less \
        ntp \
    && rm -rf /var/lib/apt/lists/*

# gpg keys listed at https://github.com/nodejs/node
RUN set -ex \
  && for key in \
    9554F04D7259F04124DE6B476D5A82AC7E37093B \
    94AE36675C464D64BAFA68DD7434390BDBE9B9C5 \
    0034A06D9D9B0064CE8ADF6BF1747F4AD2306D93 \
    FD3A5288F042B6850C66B31F09FE44734EB7990E \
    71DCFD284A79C3B38668286BC97EC7A07EDE3FC1 \
    DD8F2338BAE7501E3DD5AC78C273792F7D83545D \
    B9AE9905FFD7803F25714661B63B535A4C206CA9 \
    C4F0DFFF4E8C1A8236409D08E73BC641CC11F4C8 \
  ; do \
    gpg --keyserver ha.pool.sks-keyservers.net --recv-keys "$key"; \
  done

# install nodejs; NODE_VERSION is passed from docker-compose.yml
ARG NODE_VERSION

RUN curl -SLO "https://nodejs.org/dist/v$NODE_VERSION/node-v$NODE_VERSION-linux-x64.tar.gz" \
    && curl -SLO "https://nodejs.org/dist/v$NODE_VERSION/SHASUMS256.txt.asc" \
    && gpg --verify SHASUMS256.txt.asc \
    && grep " node-v$NODE_VERSION-linux-x64.tar.gz\$" SHASUMS256.txt.asc | sha256sum -c - \
    && tar -xzf "node-v$NODE_VERSION-linux-x64.tar.gz" -C /usr/local --strip-components=1 \
    && rm "node-v$NODE_VERSION-linux-x64.tar.gz" SHASUMS256.txt.asc

# install yarn
RUN curl -sS "https://dl.yarnpkg.com/debian/pubkey.gpg" | apt-key add - \
    && echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list \
    && apt-get update -q=2 \
    && apt-get install -y --no-install-recommends -q=2 yarn

# make directories that we mount from local
RUN mkdir -p /usr/src/sentry /etc/sentry

# change working directory to the volume we've mounted from host
WORKDIR /usr/src/sentry

# install libraries, dependencies and sentry

RUN pip install -vvv -e .[dev,tests] \
    && yarn install \
    && make develop \
    && sentry upgrade --noinput \
    && sentry createuser --email=root@localhost --password=admin --superuser --no-input

CMD [ "sentry devserver" ]
