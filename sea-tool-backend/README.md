# Ethical, social and environmental accounting tool

Developing a model-driven ethical, social and environmental accounting tool

# Docker setup (recommended - Win 10 Pro / Linux / OSX)

1. Download and install the appropriate version of Docker for your system [here](https://docker.com/products/overview).
2. copy the `.env.example` file and name it `.env`.
3. edit the env to the setting you want to use.
   - leave the `DB_TYPE` empty (SQL server is not supported yet in docker itself).
   - `ALLOWED_HOSTS` is to let django know which domains it can serve, with `DEBUG=True`, localhost will already be added. more info [here](https://docs.djangoproject.com/en/2.2/ref/settings/#allowed-hosts)
   - `CORS_ORIGIN_ALLOW_ALL` is to allow API calls from all origins. to turn it on: `=1` , turn it off `=0`.
   - When `CORS_ORIGIN_ALLOW_ALL` is off, you will need to add every origin yourself using `CORS_ORIGIN_WHITELIST` like so: `CORS_ORIGIN_WHITELIST=["https://example.com"]`. more info [here](https://pypi.org/project/django-cors-headers/)
5. run `docker-compose up --build` to build and run docker add `-d` for detached mode (Detached mode: Run containers in the background, print new container names.).
6. git hooks for development:
   - you will still need to download and install the appropriate version of Python/pip for your system [here](https://python.org/downloads/).
   - install pre-commit with `pip install pre-commit` and then afterwards run `pre-commit install`.

# Local setup

1. Download and install the appropriate version of Python/pip for your system [here](https://python.org/downloads/)
2. Install pipenv with one of the options [here](https://github.com/pypa/pipenv)
3. go to folder `backend`.
4. install packages with pipenv, which will create a virtual env with all the packages: `pipenv install --dev`.
5. copy the `.env.example` file and name it `.env`.
6. edit the env to the setting you want to use.
   - leave the `DB_TYPE` empty to use SQLite (will use a file) otherwise you will need to create a database (use utf8 format) and configurate the env.
   - `ALLOWED_HOSTS` is to let django know which domains it can serve, with `DEBUG=True`, localhost will already be added. more info [here](https://docs.djangoproject.com/en/2.2/ref/settings/#allowed-hosts)
   - `CORS_ORIGIN_ALLOW_ALL` is to allow API calls from all origins. to turn it on: `=1` , turn it off `=0`.
   - When `CORS_ORIGIN_ALLOW_ALL` is off, you will need to add every origin yourself using `CORS_ORIGIN_WHITELIST` like so: `CORS_ORIGIN_WHITELIST=["https://example.com"]`. more info [here](https://pypi.org/project/django-cors-headers/)
7. run the pipenv shell to get into the virtual env: `pipenv shell`.
8. run the migrations: `python manage.py migrate`.
9.  run the seeder: `python manage.py loaddata data`.
10. installing git hooks: run `pipenv shell` to go into the virtual environment and run `pre-commit install`. now when you make a commit, it automatically formats and checks your linting.

then you can run the server in `backend` by running the pipenv shell and starting the server.
* `pipenv shell`.
* `python manage.py runserver`.

# Unit testing and strictly typing in the project

Unit testing and typing will be slowly added to the project.

## Unit testing

Tests can be found in the `tests` folder and have `test_` as starting filename and need to be imported in the `tests/__init__`.

To run the tests use: `py manage.py test`

you can find documentation for writing unit tests in django [here](https://docs.djangoproject.com/en/3.0/topics/testing/overview/) and testing django rest framework [here](https://www.django-rest-framework.org/api-guide/testing/)

## Typing

You can check the typings with mypy, to run it use `mypy`.

you can find a guide to strictly typed in python [here](https://realpython.com/python-type-checking/)
