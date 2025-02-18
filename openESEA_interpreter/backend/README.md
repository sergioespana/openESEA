# Backend Installation



## Install Postgres (& pgAdmin)

Install Postgres online and pgAdmin to interact with postgres database etc.



## Install Python

Install Python online



### Install Python Libraries

python -m pip install -r requirements.txt



## Setup Esea DB

### Create user and database

ALTER USER postgres WITH PASSWORD 'postgres'; /* or 'admin' or 'password' */

CREATE DATABASE esea_db WITH OWNER postgres ENCODING 'utf-8';

Connect with database esea_db to see if connection works.


### Setup database structure

python manage.py migrate


### Create superuser
Create a superuser (admin username/password) for the frontend to communicate with backend database

python manage.py createsuperuser

Provide username, email, and password when asked to create super user


## Run Server

python manage.py runserver






## Save database structure

python manage.py makemigrations