#!/bin/bash

.venv/bin/alembic upgrade head

exec .venv/bin/fastapi dev homecontrol_controller/main.py --host 0.0.0.0 --port 8000