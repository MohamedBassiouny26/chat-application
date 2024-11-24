# Use an official Python image as the base
FROM python:3.12-slim
LABEL authors="Mohamed Bassiouny"
# Set the working directory

# Set up environment variables
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends tzdata curl git build-essential \
    && if [ "aarch64" = "$(arch)" ] || [ "arm64" = "$(arch)" ]; then apt-get install -y --no-install-recommends gcc python3 libpq-dev libc-dev; fi

RUN apt-get update && apt-get -y upgrade

RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/etc/poetry python3 - --version 1.8.0 && \
    cd /usr/local/bin && \
    ln -s /etc/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Install dependencies
WORKDIR /app/

COPY ./pyproject.toml ./poetry.lock* ./
RUN poetry install

RUN chmod +x bin/*
COPY . .

EXPOSE 8000

CMD ["bin/start.sh"]

