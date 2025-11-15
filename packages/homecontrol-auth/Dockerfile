# Use standard python image and copy uv over as uv image cant run entrypoint script
# gives 'exec /homecontrol-auth/docker-entrypoint.sh: no such file or directory'
FROM python:3.12
COPY --from=ghcr.io/astral-sh/uv:0.9.9 /uv /uvx /bin/

WORKDIR /homecontrol-auth

COPY homecontrol-base-api /homecontrol-base-api
COPY homecontrol-auth/homecontrol_auth ./homecontrol_auth
COPY homecontrol-auth/.python-version ./.python-version
COPY homecontrol-auth/pyproject.toml ./pyproject.toml
COPY homecontrol-auth/uv.lock ./uv.lock

RUN uv sync --locked
# RUN pip install psycopg2-binary

COPY homecontrol-auth/alembic ./alembic
COPY homecontrol-auth/alembic.ini ./alembic.ini

COPY homecontrol-auth/docker-entrypoint.sh ./docker-entrypoint.sh

ENTRYPOINT [ "/homecontrol-auth/docker-entrypoint.sh" ] 