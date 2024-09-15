
FROM python:3.12

WORKDIR /homecontrol-auth

COPY requirements-dev.txt /homecontrol-auth/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /homecontrol-auth/requirements.txt
# RUN pip install psycopg2-binary

COPY homecontrol_auth /homecontrol-auth/homecontrol_auth

CMD ["fastapi", "dev", "homecontrol_auth/main.py", "--host", "0.0.0.0", "--port", "8000"]