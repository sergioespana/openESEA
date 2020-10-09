# Using an official Python container as parent image.
FROM python:3.8-slim-buster

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

# Create directory
RUN mkdir /code
WORKDIR /code

# Install packages
RUN pip install pipenv

COPY Pipfile* /code/
RUN pipenv lock --keep-outdated -r > requirements.txt
RUN pip install -r requirements.txt

# Copy current directory content to container.
ADD . /code/

CMD ["/code/docker/prod/start.sh"]
