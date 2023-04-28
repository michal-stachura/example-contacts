# example-contacts

Example Contact Form

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

## Settings

Moved to [settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

## Basic Commands

Use below command with **sudo** if needed

- **make run** create local dev server up and running at http://127.0.0.1:8000
- **make build** build/rebuild docker images/containers
- **make migrations** create Django migration files
- **make migrate** execute migration files on database
- **make seed** build local environment + create base data admin user (admin@admin) + 50000 random objects
- **make superuser** create superuser with access to admin panel at http://127.0.0.1:8000/admin/
- **make shell** run django container with shell (python manage.py shell)
- **make cleardocker** Removes installed images/containers/volumes
- **make test** run pytests

## Prefered way to start local enironment

1. clone repo
2. run `make seed` or `sudo make seed` if needed
3. run `make run` or `sudo make run`

### Setting Up Your Users

- To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page (Email confirmation is optional). Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

- To create a **superuser account**, use this command:

      $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Type checks

Running type checks with mypy:

    $ mypy example_contacts


### Live reloading and Sass CSS compilation

Moved to [Live reloading and SASS compilation](https://cookiecutter-django.readthedocs.io/en/latest/developing-locally.html#sass-compilation-live-reloading).

## Deployment

The following details how to deploy this application.

### Docker

See detailed [cookiecutter-django Docker documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html).
