FROM python:3.8-slim-buster
ENV PYTHONUNBUFFERED 1

# Create directory
RUN mkdir /code
WORKDIR /code

# Install packages
RUN pip install pipenv

COPY Pipfile* /code/
RUN pipenv lock --keep-outdated -r > requirements.txt && pipenv lock --keep-outdated -d -r > dev-requirements.txt
RUN pip install -r requirements.txt && pip install -r dev-requirements.txt

COPY docker/dev/ .
ADD . /code/
RUN ["chmod", "+x", "docker/dev/start.sh"]
