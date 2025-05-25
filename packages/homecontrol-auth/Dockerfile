
FROM python:3.12

WORKDIR /homecontrol-auth

COPY requirements-dev.txt /homecontrol-auth/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /homecontrol-auth/requirements.txt
# RUN pip install psycopg2-binary

COPY homecontrol_auth /homecontrol-auth/homecontrol_auth

COPY alembic /homecontrol-auth/alembic
COPY alembic.ini /homecontrol-auth/alembic.ini

COPY docker-entrypoint.sh /homecontrol-auth/docker-entrypoint.sh

ENTRYPOINT [ "/homecontrol-auth/docker-entrypoint.sh" ] 