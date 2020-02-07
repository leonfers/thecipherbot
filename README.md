# THECIPHER

This project is a API for a telegram bot which is a Real Time Text-based Strategy game.

### API for THECipher Bot on telegram

## Configuring the envioriment (Linux) and the project settings

* Install Python:
```bash
sudo apt install python3
```

* Install and configure postgres

```bash
sudo apt-get install python-pip python-dev libpq-dev postgresql postgresql-contrib
sudo su - postgres
psql
CREATE DATABASE database_name;
CREATE USER myprojectuser WITH PASSWORD 'password';
ALTER ROLE myprojectuser SET client_encoding TO 'utf8';
ALTER ROLE myprojectuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE myprojectuser SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE database_name TO myprojectuser;
```

* Create a vitual envioriment and access it
```bash
python3 -m venv myvenv
source myvenv/bin/activate
```

* Configure the env variables
```bash
touch .env
nano .env
    TELEGRAM_KEY=** (Get your bot api key from the botfather on telegram)
   DEBUG=True
   SECRET_KEY=**
   DATABASE_URL=**
   DB_USER=**
   DB_PASSWORD=**
   DB_NAME = **
```

* Update pip and install the dependencies
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

__Before deploying in case you are using Debian based distros, check if the package pkg-resources==0.0.0 was created, and remove it if it is present on the requirements.txt file__

### Deploying the API to HEROKU

* Install heroku-cli and configure the deploy repo
```bash
sudo snap install --classic heroku
heroku login
heroku git:remote -a thecipher
git add .
git commit -m "Deploy da aplicação"
git push -u heroku master
heroku run python manage.py migrate
```

## Testing

## About the game

In this game, each player enters a realm with a certain number of units. When more than one player enters the same realm, they battle each other.
The objective of the game is to defeat all enemy troops.

Troops can be moved with three actions(attack, ambush and defend):
* Attacking wins ambushing.
* Ambushing wins defending.
* Defending wins attacking.

Spies only gather information and Warriors can kill other units.
You can intercept enemy messages and repair it's contents to launch counter attacks!
By defeating all enemies, you will repair the realm's peace.

## Contact Info:
* Email at leonfersn@gmail.com with the subject "THECIPHER BOT - TELEGRAM - DEV QUESTIONS"

## Info:
* This game was developed inicialy at the THEGamJam (Global Game Jam 2020) at Teresina, Piaui,  Brazil.
