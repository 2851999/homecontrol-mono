
FROM python:3.12

WORKDIR /homecontrol-controller

COPY requirements-dev.txt /homecontrol-controller/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /homecontrol-controller/requirements.txt
# RUN pip install psycopg2-binary

COPY homecontrol_controller /homecontrol-controller/homecontrol_controller

COPY alembic /homecontrol-controller/alembic
COPY alembic.ini /homecontrol-controller/alembic.ini

COPY hue_cert.pem /homecontrol-controller/hue_cert.pem

COPY docker-entrypoint.sh /homecontrol-controller/docker-entrypoint.sh

ENTRYPOINT [ "/homecontrol-controller/docker-entrypoint.sh" ] 