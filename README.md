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
python manage.py runserver:
```
to install the postgresSQL database
```sh
brew install postgresql
pip install psycopg2-binary
```
After creation you need to do a superuser and to create the database (Settings in django for the db:settings.py)
```sh
for 2FA - a check avec Mehdi
```sh
django-otp
phonenumbers
```
for the Profile picture in authentication:
```sh
pip install Pillow
```


NOTE FOR ANTHONY: 

Game selection : 

- Solo
  - Choose your side and the IA level
- Tournament
  - Create a tournament
    - Fill the information for the tournament
      - Waiting for the player / start the tournament
  - Join a tournament
    - Insert the tournament code
- Multi
  - Find a game