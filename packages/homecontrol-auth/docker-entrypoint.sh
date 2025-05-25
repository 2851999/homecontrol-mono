#!/bin/bash

alembic upgrade head

exec fastapi dev homecontrol_auth/main.py --host 0.0.0.0 --port 8000