[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


# foodgram_project

**This is an foodgram_project application that provides a REST API based on the
Django REST framework.**

The project implemented the following methods:

* Using [Django REST framework][drf].
* The authentication policy is based on the use of tokens and the [Djoser][djoser] library.
* Using [ViewSets][viewsets], [Routers][routers], ORM data sources [Serializers][serializers].
* Extensive documentation based on [ReDoc][redoc].

## Env file template

The .env file describes the following variables for creating the database
(postgresql). In particular, the following variables _must_ be set:

- `SERVER_IP` ip address of your server
- `SERVER_DOMAIN_NAME` domain name of your server
- `DJANGO_KEY` key to start django project
- `DB_ENGINE` indicate that we are working with postgresql
- `DB_NAME` database name
- `POSTGRES_USER` login to connect to the database
- `POSTGRES_PASSWORD` password to connect to the database (set your own)
- `DB_HOST` service (container) name
- `DB_PORT` port for connecting to the database

## Run tests

Before building the image, create venv and run test:

```bash
cd your_app_directory/foodgram_project
python3 -m venv venv
source env/bin/activate
pip install flake8 pep8-naming flake8-broken-line flake8-return flake8-isort
python -m flake8
```

## Installation

Build the image (run command from directory with docker-compose.yaml file):

```bash
cd your_app_directory/foodgram-project-react/infra
docker-compose up -d --build
```

Create a superuser:

```bash
docker-compose exec web python manage.py createsuperuser
```

_Important note! If you are using git bash on Windows system you should use winpty for interactive input:_

```bash
winpty docker-compose exec web python manage.py createsuperuser
```

Once everything has started up, you should be able to access the webapp via
[https://fgproject.hopto.org/](https://fgproject.hopto.org/) on your host machine:

```bash
open https://fgproject.hopto.org/
```

```bash
open https://fgproject.hopto.org/admin
```

```bash
open https://fgproject.hopto.org/api/docs
```

## Authors
- [VaeSemper](https://github.com/VaeSemper)


[//]: # (Link section not showing up when reading the README.)

[drf]: https://www.django-rest-framework.org/
[Djoser]: https://djoser.readthedocs.io/en/latest/index.html
[serializers]: https://www.django-rest-framework.org/api-guide/serializers/#modelserializer
[viewsets]: https://www.django-rest-framework.org/api-guide/viewsets/#viewsets
[routers]: https://www.django-rest-framework.org/api-guide/routers/
[redoc]: https://redocly.github.io/redoc/
