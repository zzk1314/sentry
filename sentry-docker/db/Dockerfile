FROM postgres:9.4
# Use postgres/example user/password credentials
#RUN ["createdb", "sentry"]

COPY ./db/docker-entrypoint.sh /docker-entrypoint-initdb.d/
