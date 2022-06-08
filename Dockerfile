FROM python:3.8.3

WORKDIR /usr/src/djangoProject

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install netcat -y
RUN apt-get upgrade -y && apt-get install postgresql gcc python3-dev musl-dev -y
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

COPY ./pyproject.toml ./poetry.lock* /usr/src/djangoProject/

RUN poetry install

COPY ./entrypoint.sh /usr/src/djangoProject/

COPY . /usr/src/djangoProject/

RUN chmod 755 /usr/src/djangoProject/prestart.sh