FROM python3.12:latest
LABEL authors="shift-python-software"

ARG UID=1000
ARG GID=1000
ARG VERSION=1.0.0

RUN apt-get update && apt-get install -y procps libpq-dev
RUN groupadd --gid $GID app && useradd --uid $UID --gid $GID app
WORKDIR /app
USER app
COPY . /app
RUN pip install -r requirements.txt
