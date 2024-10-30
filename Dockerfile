FROM python:3.12.6-slim

ENV PYTHONDONTWRITEBYTECODE 1 # Prevents Python from writing pyc files to disc
ENV PYTHONFAULTHANDLER 1 # Makes Python more verbose in case of an error
ENV PIPENV_VENV_IN_PROJECT 1

RUN apt-get update && \
    apt-get install -y gdal-bin libgdal-dev

RUN pip install pipenv

RUN useradd -ms /bin/bash admin

USER admin

WORKDIR /home/admin/app

CMD tail -f /dev/null

