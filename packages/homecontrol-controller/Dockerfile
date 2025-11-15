# Use standard python image and copy uv over as uv image cant run entrypoint script
# gives 'exec /homecontrol-controller/docker-entrypoint.sh: no such file or directory'
FROM python:3.12
COPY --from=ghcr.io/astral-sh/uv:0.9.9 /uv /uvx /bin/

WORKDIR /homecontrol-controller

COPY homecontrol-base-api /homecontrol-base-api
COPY homecontrol-controller/homecontrol_controller ./homecontrol_controller
COPY homecontrol-controller/.python-version ./.python-version
COPY homecontrol-controller/pyproject.toml ./pyproject.toml
COPY homecontrol-controller/uv.lock ./uv.lock

RUN uv sync --locked
# RUN pip install psycopg2-binary

COPY homecontrol-controller/alembic ./alembic
COPY homecontrol-controller/alembic.ini ./alembic.ini

COPY homecontrol-controller/hue_cert.pem ./hue_cert.pem

COPY homecontrol-controller/docker-entrypoint.sh ./docker-entrypoint.sh

ENTRYPOINT [ "/homecontrol-controller/docker-entrypoint.sh" ] 