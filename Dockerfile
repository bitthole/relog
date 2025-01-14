FROM python:3.12

EXPOSE 80

WORKDIR /app

# Create a non-root user and group (e.g., "uwsgi")
RUN groupadd -r uwsgigroup && useradd -r -g uwsgigroup uwsgi

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./src /app/

# CMD [ "uwsgi", "--http-socket", "0.0.0.0:80", \
#                "--plugins", "python3", \
#                "--protocol", "uwsgi", \
#                "--wsgi", "app:application" ]

CMD [ "uwsgi", "--http", ":80", \
               "--uid", "uwsgi", \
               "--master", "--processes", "4", \
               "--wsgi-file", "app.py", \
               "--callable", "application", \
               "--module", "app:application" ]
