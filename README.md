# Transcendence

## Project Structure

The project is organized as follows: **TO BE UPDATED**

- `backend/`: Contains the main backend module of project.
  - `djangoProject/`: The main Django project directory.
    - `settings.py`: Configuration settings for the project.
    - `urls.py`: URL declarations for the Django project.
    - `wsgi.py`: WSGI configuration for deploying the Django project.
  - `API/`: Contains the API application.
    - `apps.py`: Configuration for the API application.
  - `authentication/`: Contains the authentication application.
    - `apps.py`: Configuration for the authentication application.
  - `game/`: Contains the game application.
    - `apps.py`: Configuration for the game application.

- `manage.py`: Command-line utility for administrative tasks.

```sh
python manage.py runserver